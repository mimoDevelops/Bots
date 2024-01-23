import tweepy
from pymongo import MongoClient
import time

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client['twitter_bot_db']
collection = db['user_details']

# Twitter authentication
auth = tweepy.OAuthHandler("************************", "************************")
auth.set_access_token("************************-************************", "************************")
api = tweepy.API(auth)

# Function to get authenticated user details and store in MongoDB
def get_authenticated_user_details():
    try:
        user = api.verify_credentials()
        if user:
            user_details = {
                "Username": user.screen_name,
                "Name": user.name,
                "Location": user.location,
                "Followers Count": user.followers_count,
                "Pinned Tweet ID": user.status.id_str if user.status else None,
                "Bio": user.description
            }
            collection.insert_one({**user_details, 'timestamp': time.time()})
            return user_details
        else:
            return "Unable to fetch user details."
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        collection.insert_one({'status': 'error', 'error_message': error_msg, 'timestamp': time.time()})
        return error_msg

# Fetch and print user details
user_details = get_authenticated_user_details()
print(user_details)
