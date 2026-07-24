from bson import ObjectId
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from database.mongodb import violations_collection
from .serializers import ViolationSerializer
from bson.errors import InvalidId
from database.violation_service import (
    get_all_violations,
    get_violation_by_id,
    add_violation,
    update_violation as update_violation_service,
    delete_violation as delete_violation_service,
)

def check_admin_session(request):
    if "user_id" not in request.session:
        return Response(
            {"message": "Unauthorized. Please login first."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return None

def violation_to_dict(violation):
    return {
        "id": str(violation["_id"]),
        "vehicle_number": violation.get("vehicle_number"),
        "owner_name": violation.get("owner_name"),
        "violation_type": violation.get("violation_type"),
        "location": violation.get("location"),
        "officer_name": violation.get("officer_name"),
        "fine_amount": violation.get("fine_amount"),
        "status": violation.get("status"),
        "date": violation.get("date")
    } 
    
# ==========================
# GET ALL VIOLATIONS
# ==========================    
@api_view(["GET"])
def get_violations(request):

    auth = check_admin_session(request)
    if auth:
        return auth

    violations = list(violations_collection.find())

    data = [violation_to_dict(v) for v in violations]

    serializer = ViolationSerializer(data, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    ) 
    
# ==========================
# GET SINGLE VIOLATION
# ==========================

@api_view(["GET"])
def get_violation(request, violation_id):

    auth = check_admin_session(request)
    if auth:
        return auth

    # Validate ObjectId
    try:
        object_id = ObjectId(violation_id)
    except InvalidId:
        return Response(
            {"message": "Invalid Violation ID"},
            status=status.HTTP_400_BAD_REQUEST
        )

    violation = violations_collection.find_one(
        {"_id": object_id}
    )

    if not violation:
        return Response(
            {"message": "Violation Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )

    data = violation_to_dict(violation)

    serializer = ViolationSerializer(data)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )    

# ==========================
# CREATE VIOLATION
# ==========================

@api_view(["POST"])
def create_violation(request):
    auth = check_admin_session(request)
    if auth:
        return auth

    data = request.data

    # Validate Fine Amount
    try:
        fine_amount = int(data.get("fine_amount"))
    except (TypeError, ValueError):
        return Response(
            {"message": "Invalid Fine Amount"},
            status=status.HTTP_400_BAD_REQUEST
        )

    violation = {
        "vehicle_number": data.get("vehicle_number", "").upper(),
        "owner_name": data.get("owner_name"),
        "violation_type": data.get("violation_type"),
        "location": data.get("location"),
        "officer_name": data.get("officer_name"),
        "fine_amount": fine_amount,
        "status": data.get("status", "Pending"),
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    result = violations_collection.insert_one(violation)

    return Response(
        {
            "message": "Violation Added Successfully",
            "id": str(result.inserted_id)
        },
        status=status.HTTP_201_CREATED
    )
    
# ==========================
# UPDATE VIOLATION
# ==========================

@api_view(["PUT"])
def update_violation(request, violation_id):

    auth = check_admin_session(request)
    if auth:
        return auth

    # Validate ObjectId
    try:
        object_id = ObjectId(violation_id)
    except InvalidId:
        return Response(
            {"message": "Invalid Violation ID"},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data

    vehicle_number = data.get("vehicle_number")
    owner_name = data.get("owner_name")
    violation_type = data.get("violation_type")
    location = data.get("location")
    officer_name = data.get("officer_name")
    fine_amount = data.get("fine_amount")
    status_value = data.get("status")

    # Validation
    if not vehicle_number:
        return Response(
            {"message": "Vehicle Number is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not owner_name:
        return Response(
            {"message": "Owner Name is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not violation_type:
        return Response(
            {"message": "Violation Type is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not location:
        return Response(
            {"message": "Location is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not officer_name:
        return Response(
            {"message": "Officer Name is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if fine_amount is None:
        return Response(
            {"message": "Fine Amount is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate Fine Amount
    try:
        fine_amount = int(fine_amount)
    except (TypeError, ValueError):
        return Response(
            {"message": "Invalid Fine Amount"},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = violations_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "vehicle_number": vehicle_number.upper(),
                "owner_name": owner_name,
                "violation_type": violation_type,
                "location": location,
                "officer_name": officer_name,
                "fine_amount": fine_amount,
                "status": status_value
            }
        }
    )

    if result.matched_count == 0:
        return Response(
            {"message": "Violation Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {"message": "Violation Updated Successfully"},
        status=status.HTTP_200_OK
    )
    
# ==========================
# DELETE VIOLATION
# ==========================

@api_view(["DELETE"])
def delete_violation(request, violation_id):

    auth = check_admin_session(request)
    if auth:
        return auth

    # Validate ObjectId
    try:
        object_id = ObjectId(violation_id)
    except InvalidId:
        return Response(
            {"message": "Invalid Violation ID"},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = violations_collection.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        return Response(
            {"message": "Violation Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {"message": "Violation Deleted Successfully"},
        status=status.HTTP_200_OK
    )
    
# ==========================
# DASHBOARD STATISTICS
# ==========================

@api_view(["GET"])
def dashboard_statistics(request):

    auth = check_admin_session(request)
    if auth:
        return auth

    total = violations_collection.count_documents({})

    paid = violations_collection.count_documents({
        "status": "Paid"
    })

    pending = violations_collection.count_documents({
        "status": "Pending"
    })

    total_fine = 0

    violations = violations_collection.find()

    for violation in violations:
        total_fine += violation.get("fine_amount", 0)

    return Response(
        {
            "total_violations": total,
            "paid_violations": paid,
            "pending_violations": pending,
            "total_fine_amount": total_fine
        },
        status=status.HTTP_200_OK
    )
# ==========================
# API HOME
# ==========================

@api_view(["GET"])
def api_home(request):

    auth = check_admin_session(request)
    if auth:
        return auth

    return Response(
        {
            "message": "Welcome to TrafficEye REST API",
            "status": "Running",
            "version": "1.0",
            "available_endpoints": {
                "Dashboard": "/api/dashboard/",
                "Get All Violations": "/api/violations/",
                "Get Single Violation": "/api/violations/<id>/",
                "Create Violation": "/api/violations/create/",
                "Update Violation": "/api/violations/update/<id>/",
                "Delete Violation": "/api/violations/delete/<id>/"
            }
        },
        status=status.HTTP_200_OK
    )
    