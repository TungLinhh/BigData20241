
# Real-time Social Media Sentiment Analysis

A scalable system for real-time sentiment analysis of social media data using Apache Spark, Kafka, and Cassandra.

## Architecture

```
Twitter API → Kafka → Spark Streaming → Cassandra
                        ↓
                      HDFS
```

## Prerequisites

- Docker & Docker Compose
- Python 3.8+
- Twitter Developer Account
- 8GB+ RAM

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-media-sentiment
cd social-media-sentiment
```

2. Configure credentials:
```bash
cp config/twitter_credentials.json.example config/twitter_credentials.json
# Edit twitter_credentials.json with your Twitter API credentials
```

3. Start the infrastructure:
```bash
docker-compose up -d
```

4. Initialize services:
```bash
docker exec -it kafka /scripts/init-kafka.sh
docker exec -it cassandra /scripts/init-cassandra.sh
```

5. Start processing:
```bash
python src/data_ingestion.py
```

## Configuration

### Twitter API
Edit 

twitter_credentials.json

:
```json
{
    "consumer_key": "YOUR_KEY",
    "consumer_secret": "YOUR_SECRET",
    "access_token": "YOUR_TOKEN",
    "access_token_secret": "YOUR_TOKEN_SECRET"
}
```

### Spark Configuration
Edit 

spark_config.json

 for tuning:
```json
{
    "master": "spark://spark-master:7077",
    "checkpoint_dir": "/tmp/checkpoint"
}
```

## Monitoring

- Spark UI: http://localhost:8080
- Kafka Manager: http://localhost:9000
- HDFS NameNode: http://localhost:9870
- Cassandra: localhost:9042

## Data Schema

### Cassandra
```sql
CREATE TABLE tweets (
    id UUID PRIMARY KEY,
    text TEXT,
    sentiment TEXT,
    timestamp TIMESTAMP
)
```

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

Run integration tests:
```bash
python -m pytest tests/ --integration
```

## Troubleshooting

### Common Issues

1. Kafka Connection:
```bash
docker-compose logs kafka
```

2. Spark Job Failures:
```bash
docker-compose logs spark-master
```

3. Reset System:
```bash
docker-compose down -v
docker-compose up -d
```

## Performance Tuning

1. Kafka:
- Partitions: 3 (default)
- Replication: 1 (development)

2. Spark:
- Memory: 2G per worker
- Parallelism: 3 partitions

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## Acknowledgments

- Apache Spark
- Apache Kafka
- Apache Cassandra
- Twitter API
```
