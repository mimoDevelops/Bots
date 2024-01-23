import tweepy
from pymongo import MongoClient
import time

# MongoDB connection
client = MongoClient('localhost', 27017)  # Adjust host and port as needed
db = client['twitter_bot_db']  # Database name
collection = db['tweet_posts']  # Collection name

# Twitter Authentication
consumer_key = '************************'
consumer_secret = '************************'
access_token = '************************'
access_token_secret = '************************'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function to post a tweet and log in MongoDB
def post_tweet(text):
    try:
        tweet = api.update_status(text)
        print("Tweet posted successfully")
        collection.insert_one({'tweet_text': text, 'status': 'posted', 'tweet_id': tweet.id_str, 'timestamp': time.time()})
    except Exception as e:
        print(f"Error posting tweet: {e}")
        collection.insert_one({'tweet_text': text, 'status': 'error', 'error_message': str(e), 'timestamp': time.time()})

# Example usage
post_tweet("YeLLLLO twittter")
