from pymongo import MongoClient
from decouple import config

MONGODB_URI = config("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client.get_default_database()
