#!/bin/bash

# Initialize Spark
spark-submit --deploy-mode client --master spark://spark-master:7077 /src/stream_processing.py