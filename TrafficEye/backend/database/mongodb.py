from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["trafficeye"]

# Collections
users_collection = db["users"]

print("MongoDB Connected Successfully")