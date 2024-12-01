import unittest
from kafka import KafkaConsumer
import json
import time

class TestDataIngestion(unittest.TestCase):
    def setUp(self):
        self.consumer = KafkaConsumer('social-media-raw', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')

    def test_data_ingestion(self):
        # Wait for some data to be ingested
        time.sleep(10)
        for message in self.consumer:
            data = json.loads(message.value.decode())
            self.assertIn('id_str', data)
            self.assertIn('text', data)
            break

if __name__ == '__main__':
    unittest.main()