import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set. Add it to your .env file.")

# Create a single global client (recommended)
_client = MongoClient(MONGO_URI)
_db = _client[MONGO_DB_NAME]

def get_db():
    """Return the main database object."""
    return _db

def get_collection(name: str):
    """Helper to get a collection by name."""
    return _db[name]
