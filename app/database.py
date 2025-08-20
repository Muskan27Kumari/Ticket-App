from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.DATABASE_URL)
db = client.get_default_database()