from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid

# Load Cassandra config
with open('/config/cassandra_config.json', 'r') as f:
    cassandra_config = json.load(f)

auth_provider = PlainTextAuthProvider(username=cassandra_config['username'], password=cassandra_config['password'])
cluster = Cluster(contact_points=[cassandra_config['contact_points']], auth_provider=auth_provider)
session = cluster.connect(cassandra_config['keyspace'])

def save_to_cassandra(data):
    session.execute(
        """
        INSERT INTO tweets (id, text, sentiment, timestamp)
        VALUES (%s, %s, %s, %s)
        """,
        (uuid.UUID(data['id']), data['text'], data['sentiment'], data['timestamp'])
    )