from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StringType, StructType, StructField, TimestampType

# Load Spark config
with open('/config/spark_config.json', 'r') as f:
    spark_config = json.load(f)

spark = SparkSession.builder \
    .appName("SentimentAnalysis") \
    .master(spark_config['master']) \
    .config("spark.streaming.kafka.maxRatePerPartition", 100) \
    .config("spark.sql.shuffle.partitions", 3) \
    .getOrCreate()

# Define schema for incoming data
schema = StructType([
    StructField("id_str", StringType(), True),
    StructField("text", StringType(), True),
    StructField("created_at", TimestampType(), True)
])

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", spark_config['bootstrap_servers']) \
    .option("subscribe", "social-media-raw") \
    .load()

# Parse JSON data
df = df.selectExpr("CAST(value AS STRING) as json").select(from_json(col("json"), schema).alias("data")).select("data.*")

# Sentiment analysis UDF
def analyze_sentiment(text):
    # Placeholder for actual sentiment analysis logic
    return "positive" if "good" in text.lower() else "negative"

analyze_sentiment_udf = udf(analyze_sentiment, StringType())

# Apply sentiment analysis
df = df.withColumn("sentiment", analyze_sentiment_udf(col("text")))

# Write to Kafka
query = df.selectExpr("id_str as key", "to_json(struct(*)) as value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", spark_config['bootstrap_servers']) \
    .option("topic", "sentiment-processed") \
    .outputMode("append") \
    .start()

query.awaitTermination()