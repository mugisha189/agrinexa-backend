from pymongo import MongoClient
from app.settings import MONGODB_URL

client = MongoClient(MONGODB_URL)

db = client.get_default_database()
