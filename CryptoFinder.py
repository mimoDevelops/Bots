import requests
import time
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client['crypto_bot_db']
collection = db['crypto_prices']

def get_crypto_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[coin_id]['usd']

def main():
    coin_name = input("Enter the cryptocurrency name (e.g., bitcoin or ethereum): ").lower()
    
    while True:
        try:
            coin_id = coin_name.replace(" ", "-")
            price = get_crypto_price(coin_id)
            print(f"The current price of {coin_name.capitalize()} is ${price:}")
            collection.insert_one({'coin_id': coin_id, 'price': price, 'timestamp': time.time()})
        except KeyError:
            print(f"Could not find information for {coin_name}. Please enter a valid cryptocurrency name.")
            collection.insert_one({'coin_id': coin_id, 'status': 'error', 'timestamp': time.time()})
        
        time.sleep(60)

if __name__ == "__main__":
    main()
