# db_config.py
from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'candidate_db'
COLLECTION_NAME = 'candidates'

def get_db_connection():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return client, db
