import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = None
DB = None

try:
    client = MongoClient(MONGO_URI)
    DB = client['Project']
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

def get_db():
    if DB is None:
        raise Exception("Database connection is not established.")
    return DB

DB = get_db()
