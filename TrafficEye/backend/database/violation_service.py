from bson import ObjectId
from bson.errors import InvalidId
from database.mongodb import violations_collection
from datetime import datetime
from collections import defaultdict


# -------------------------------
# Create
# -------------------------------
def add_violation(data):
    """Insert a new traffic violation."""
    return violations_collection.insert_one(data)

# -------------------------------
# Read
# -------------------------------
def get_all_violations():
    return list(
        violations_collection.find().sort("date", -1)
    )


def get_violation_by_id(violation_id):
    try:
        return violations_collection.find_one(
            {"_id": ObjectId(violation_id)}
        )
    except (InvalidId, TypeError):
        return None


# -------------------------------
# Update
# -------------------------------
def update_violation(violation_id, data):
    try:
        return violations_collection.update_one(
            {"_id": ObjectId(violation_id)},
            {"$set": data}
        )
    except (InvalidId, TypeError):
        return None

# -------------------------------
# Delete
# -------------------------------
def delete_violation(violation_id):
    try:
        return violations_collection.delete_one(
            {"_id": ObjectId(violation_id)}
        )
    except (InvalidId, TypeError):
        return None


# -------------------------------
# Search
# -------------------------------
def search_by_vehicle(vehicle_number):
    return list(
        violations_collection.find(
            {
                "vehicle_number": {
                    "$regex": vehicle_number,
                    "$options": "i"
                }
            }
        ).sort("date", -1)
    )

def search_by_location(location):
    return list(
        violations_collection.find(
            {
                "location": {
                    "$regex": location,
                    "$options": "i"
                }
            }
        ).sort("date", -1)
    )


def search_by_violation_type(violation_type):
    return list(
        violations_collection.find(
            {
                "violation_type": {
                    "$regex": violation_type,
                    "$options": "i"
                }
            }
        ).sort("date", -1)
    )


# -------------------------------
# Dashboard Statistics
# -------------------------------
def get_total_violations():
    return violations_collection.count_documents({})


def get_pending_fines():
    return violations_collection.count_documents(
        {"status": "Pending"}
    )


def get_paid_fines():
    return violations_collection.count_documents(
        {"status": "Paid"}
    )


def get_recent_violations(limit=5):
    return list(
        violations_collection.find()
        .sort("date", -1)
        .limit(limit)
    )


# -------------------------------
# Reports
# -------------------------------
def get_filtered_violations(query, sort="newest"):
    cursor = violations_collection.find(query)

    if sort == "oldest":
        cursor = cursor.sort("date", 1)
    else:
        cursor = cursor.sort("date", -1)

    return cursor


def mark_fine_paid(violation_id):
    try:
        return violations_collection.update_one(
            {"_id": ObjectId(violation_id)},
            {
                "$set": {
                    "status": "Paid"
                }
            }
        )
    except (InvalidId, TypeError):
        return None

def count_filtered_violations(query: dict) -> int:
    """Return the number of violations matching the given filter."""
    return violations_collection.count_documents(query)

# -------------------------------
# Report Helper Functions
# -------------------------------

def get_total_collection():
    total = 0

    violations = violations_collection.find({"status": "Paid"})

    for violation in violations:
        try:
            total += int(violation.get("fine_amount", 0))
        except (TypeError, ValueError):
            continue

    return total

def search_vehicle_report(vehicle_number):
    return list(
        violations_collection.find(
            {
                "vehicle_number": {
                    "$regex": vehicle_number,
                    "$options": "i"
                }
            }
        ).sort("date", -1)
    )


def search_officer_report(officer_name):
    return list(
        violations_collection.find(
            {
                "officer_name": {
                    "$regex": officer_name,
                    "$options": "i"
                }
            }
        ).sort("date", -1)
    )


def get_pending_violations():
    return list(
        violations_collection.find(
            {"status": "Pending"}
        ).sort("date", -1)
    )


def get_paid_violations():
    return list(
        violations_collection.find(
            {"status": "Paid"}
        ).sort("date", -1)
    )


def get_daily_report(date):
    return list(
        violations_collection.find(
            {"date": date}
        ).sort("date", -1)
    )

def get_monthly_violation_stats():
    """
    Returns the number of violations for each month.
    """

    monthly_data = defaultdict(int)

    violations = violations_collection.find()

    for violation in violations:
        try:
            date = violation.get("date")

            if not date:
                continue

            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d")

            month = date.strftime("%b")

            monthly_data[month] += 1

        except Exception:
            continue

    months = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    return [
        {
            "month": month,
            "count": monthly_data.get(month, 0)
        }
        for month in months
    ]

def get_violation_type_stats():
    """
    Returns count of each violation type.
    """

    pipeline = [
        {
            "$group": {
                "_id": "$violation_type",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    result = violations_collection.aggregate(pipeline)

    return [
        {
            "type": item["_id"],
            "count": item["count"]
        }
        for item in result
    ]

def get_payment_status_stats():
    """
    Returns paid and pending counts.
    """

    return {
        "Paid": get_paid_fines(),
        "Pending": get_pending_fines()
    }