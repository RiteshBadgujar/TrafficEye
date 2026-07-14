from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read values from .env
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

try:
    # Create MongoDB client
    client = MongoClient(MONGO_URI)

    # Select database
    db = client[DATABASE_NAME]

    # Verify connection
    client.admin.command("ping")

    print("===================================")
    print("MongoDB Connected Successfully")
    print(f"Database : {DATABASE_NAME}")
    print("===================================")

except Exception as e:
    print("MongoDB Connection Failed")
    print(e)