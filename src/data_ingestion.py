import json
from kafka import KafkaProducer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

# Load Kafka config
with open('/config/kafka_config.json', 'r') as f:
    kafka_config = json.load(f)

producer = KafkaProducer(bootstrap_servers=kafka_config['bootstrap_servers'])

class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        producer.send('social-media-raw', key=tweet['id_str'].encode(), value=data.encode())
        return True

    def on_error(self, status):
        print(f"Error: {status}")

# Twitter API credentials
with open('/config/twitter_credentials.json', 'r') as f:
    twitter_credentials = json.load(f)

auth = OAuthHandler(twitter_credentials['consumer_key'], twitter_credentials['consumer_secret'])
auth.set_access_token(twitter_credentials['access_token'], twitter_credentials['access_token_secret'])

# Start streaming
stream = Stream(auth, TwitterStreamListener())
stream.filter(track=["#example"])