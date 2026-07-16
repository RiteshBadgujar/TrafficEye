from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["trafficeye"]

users_collection = db["users"]

violations_collection = db["violations"]

print("MongoDB Connected Successfully")