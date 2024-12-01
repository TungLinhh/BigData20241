import unittest
from pyspark.sql import SparkSession
import json

class TestSparkProcessing(unittest.TestCase):
    def setUp(self):
        self.spark = SparkSession.builder \
            .appName("TestSparkProcessing") \
            .master("local[2]") \
            .getOrCreate()

    def test_sentiment_analysis(self):
        from src.spark_processing import analyze_sentiment
        self.assertEqual(analyze_sentiment("This is a good tweet"), "positive")
        self.assertEqual(analyze_sentiment("This is a bad tweet"), "negative")

if __name__ == '__main__':
    unittest.main()