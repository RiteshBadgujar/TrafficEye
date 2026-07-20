from database.mongodb import violations_collection


def add_violation(data):
    return violations_collection.insert_one(data)


def get_all_violations():
    return list(violations_collection.find())


def get_violation(violation_id):
    return violations_collection.find_one({"_id": violation_id})


def update_violation(violation_id, data):
    return violations_collection.update_one(
        {"_id": violation_id},
        {"$set": data}
    )


def delete_violation(violation_id):
    return violations_collection.delete_one({"_id": violation_id})


def search_by_vehicle(vehicle_no):
    return list(
        violations_collection.find(
            {"vehicle_no": vehicle_no}
        )
    )


def search_by_location(location):
    return list(
        violations_collection.find(
            {"location": location}
        )
    )


def search_by_violation_type(violation_type):
    return list(
        violations_collection.find(
            {"violation_type": violation_type}
        )
    )


def get_pending_fines():
    return violations_collection.count_documents(
        {"status": "Pending"}
    )


def get_paid_fines():
    return violations_collection.count_documents(
        {"status": "Paid"}
    )


def get_total_violations():
    return violations_collection.count_documents({})


def get_recent_violations(limit=5):
    return list(
        violations_collection.find()
        .sort("_id", -1)
        .limit(limit)
    )