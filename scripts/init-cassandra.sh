#!/bin/bash

# Initialize Cassandra keyspace and table
cqlsh -e "CREATE KEYSPACE IF NOT EXISTS sentiment WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};"
cqlsh -e "USE sentiment; CREATE TABLE IF NOT EXISTS tweets (id UUID PRIMARY KEY, text TEXT, sentiment TEXT, timestamp TIMESTAMP);"