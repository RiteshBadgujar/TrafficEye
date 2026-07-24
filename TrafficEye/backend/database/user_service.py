from database.mongodb import users_collection
from bson import ObjectId

def register_user(user):
    """
    Register a new user
    """
    return users_collection.insert_one(user)


def get_user_by_email(email):
    """
    Find user by email
    """
    return users_collection.find_one({
        "email": email
    })


def get_user_by_id(user_id):
    """
    Find user by ID
    """
    return users_collection.find_one({
        "_id": ObjectId(user_id)
    })


def get_all_users():
    """
    Get all users
    """
    return list(users_collection.find())


def get_total_users():
    """
    Count total users
    """
    return users_collection.count_documents({})


def update_user(email, updated_data):
    """
    Update user profile
    """
    return users_collection.update_one(
        {"email": email},
        {
            "$set": updated_data
        }
    )


def change_password(email, hashed_password):
    """
    Change user password
    """
    return users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "password": hashed_password
            }
        }
    )


def delete_user(email):
    """
    Delete user
    """
    return users_collection.delete_one({
        "email": email
    })
    
from database.mongodb import users_collection

def get_total_officers():
    return users_collection.count_documents(
        {
            "role": "Officer"
        }
    )