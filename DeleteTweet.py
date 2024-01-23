import tweepy
import time
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('localhost', 27017)  # Connects to the MongoDB server on the default port
db = client['twitter_bot_db']  # Database name (create if it doesn't exist)
collection = db['tweet_deletions']  # Collection name (create if it doesn't exist)

# Authenticate to Twitter
auth = tweepy.OAuthHandler("************************", "************************")
auth.set_access_token("************************-************************", "************************")
api = tweepy.API(auth)

# Function to delete a tweet and store the result in MongoDB
def delete_tweet(tweet_id):
    try:
        api.destroy_status(tweet_id)
        print("Tweet deleted successfully")
        collection.insert_one({'tweet_id': tweet_id, 'status': 'deleted', 'timestamp': time.time()})
    except Exception as e:
        print(f"Error deleting tweet: {e}")
        collection.insert_one({'tweet_id': tweet_id, 'status': 'error', 'error_message': str(e), 'timestamp': time.time()})

# Example usage
time.sleep(10)  # Wait for a bit before deleting

# Replace with the ID of the tweet you want to delete
tweet_id_to_delete = '123456789'
delete_tweet(tweet_id_to_delete)
