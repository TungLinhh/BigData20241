#!/bin/bash

# Create Kafka topics
kafka-topics.sh --create --topic social-media-raw --bootstrap-server kafka:9092 --replication-factor 1 --partitions 3
kafka-topics.sh --create --topic sentiment-processed --bootstrap-server kafka:9092 --replication-factor 1 --partitions 3