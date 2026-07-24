from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "trafficeye")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file.")

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    # Verify the connection
    client.admin.command("ping")

    db = client[DATABASE_NAME]

    users_collection = db["users"]
    violations_collection = db["violations"]

    print("✅ MongoDB Connected Successfully")

except ConnectionFailure:
    print("❌ Failed to connect to MongoDB.")
    raise