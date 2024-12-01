import unittest
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid

class TestStorage(unittest.TestCase):
    def setUp(self):
        auth_provider = PlainTextAuthProvider(username="cassandra", password="cassandra")
        self.cluster = Cluster(contact_points=["cassandra"], auth_provider=auth_provider)
        self.session = self.cluster.connect("sentiment")

    def test_save_to_cassandra(self):
        from src.storage import save_to_cassandra
        data = {
            "id": str(uuid.uuid4()),
            "text": "Test tweet",
            "sentiment": "positive",
            "timestamp": "2023-10-01 10:00:00"
        }
        save_to_cassandra(data)

        result = self.session.execute("SELECT * FROM tweets WHERE id = %s", [uuid.UUID(data["id"])])
        self.assertEqual(len(result.current_rows), 1)
        row = result.current_rows[0]
        self.assertEqual(row.text, "Test tweet")
        self.assertEqual(row.sentiment, "positive")

if __name__ == '__main__':
    unittest.main()