#!/bin/bash

# Initialize HDFS directories
hadoop fs -mkdir -p /user/hadoop/raw
hadoop fs -mkdir -p /user/hadoop/processed