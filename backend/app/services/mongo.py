# app/services/mongo.py (add at top)
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "text_retrived")
MONGO_SEARCH_INDEX = os.getenv("MONGO_SEARCH_INDEX", "default") 

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set. Add it to your .env file.")

_client = MongoClient(MONGO_URI)
_db = _client[MONGO_DB_NAME]

def get_db():
    return _db

def get_collection(name: str):
    return _db[name]
