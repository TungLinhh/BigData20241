from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window
from pyspark.sql.types import StringType, StructType, StructField, TimestampType
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Load Spark config
with open('/config/spark_config.json', 'r') as f:
    spark_config = json.load(f)

# Load Cassandra config
with open('/config/cassandra_config.json', 'r') as f:
    cassandra_config = json.load(f)

spark = SparkSession.builder \
    .appName("StreamProcessing") \
    .master(spark_config['master']) \
    .config("spark.streaming.kafka.maxRatePerPartition", 100) \
    .config("spark.sql.shuffle.partitions", 3) \
    .getOrCreate()

# Define schema for incoming data
schema = StructType([
    StructField("id_str", StringType(), True),
    StructField("text", StringType(), True),
    StructField("created_at", TimestampType(), True),
    StructField("sentiment", StringType(), True)
])

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", spark_config['bootstrap_servers']) \
    .option("subscribe", "sentiment-processed") \
    .load()

# Parse JSON data
df = df.selectExpr("CAST(value AS STRING) as json").select(from_json(col("json"), schema).alias("data")).select("data.*")

# Define window duration
window_duration = "10 minutes"
slide_duration = "5 minutes"

# Apply windowing
windowed_df = df.groupBy(window(col("created_at"), window_duration, slide_duration), col("sentiment")) \
    .count() \
    .withColumnRenamed("count", "tweet_count")

# Write to Cassandra
auth_provider = PlainTextAuthProvider(username=cassandra_config['username'], password=cassandra_config['password'])
cluster = Cluster(contact_points=[cassandra_config['contact_points']], auth_provider=auth_provider)
session = cluster.connect(cassandra_config['keyspace'])

def write_to_cassandra(batch_df, batch_id):
    batch_df.write \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="tweets", keyspace=cassandra_config['keyspace']) \
        .mode("append") \
        .save()

query = windowed_df.writeStream \
    .foreachBatch(write_to_cassandra) \
    .outputMode("update") \
    .start()

query.awaitTermination()