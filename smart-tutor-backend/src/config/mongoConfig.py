import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
DB_NAME = "smart_tutor"

client = None
db = None

def get_mongo_client():
    global client, db
    if client is None:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DB_NAME]
    return client

def get_mongo_db():
    global client, db
    if client is None:
        get_mongo_client()
    return db
