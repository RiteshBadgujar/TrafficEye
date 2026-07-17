from bson import ObjectId
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from database.mongodb import violations_collection
from .serializers import ViolationSerializer


# ==========================
# GET ALL VIOLATIONS
# ==========================

@api_view(["GET"])
def get_violations(request):

    violations = list(violations_collection.find())

    data = []

    for violation in violations:

        data.append({

            "id": str(violation["_id"]),
            "vehicle_number": violation.get("vehicle_number"),
            "owner_name": violation.get("owner_name"),
            "violation_type": violation.get("violation_type"),
            "location": violation.get("location"),
            "officer_name": violation.get("officer_name"),
            "fine_amount": violation.get("fine_amount"),
            "status": violation.get("status"),
            "date": violation.get("date")

        })

    serializer = ViolationSerializer(data, many=True)

    return Response(serializer.data)


# ==========================
# GET SINGLE VIOLATION
# ==========================

@api_view(["GET"])
def get_violation(request, violation_id):

    violation = violations_collection.find_one(
        {"_id": ObjectId(violation_id)}
    )

    if not violation:

        return Response(
            {"message": "Violation Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )

    data = {

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

    serializer = ViolationSerializer(data)

    return Response(serializer.data)


# ==========================
# CREATE VIOLATION
# ==========================

@api_view(["POST"])
def create_violation(request):

    data = request.data

    violation = {

        "vehicle_number": data.get("vehicle_number", "").upper(),
        "owner_name": data.get("owner_name"),
        "violation_type": data.get("violation_type"),
        "location": data.get("location"),
        "officer_name": data.get("officer_name"),
        "fine_amount": int(data.get("fine_amount")),
        "status": data.get("status", "Pending"),
        "date": datetime.now().strftime("%d-%m-%Y")

    }

    result = violations_collection.insert_one(violation)

    return Response({

        "message": "Violation Added Successfully",

        "id": str(result.inserted_id)

    })


# ==========================
# UPDATE VIOLATION
# ==========================

@api_view(["PUT"])
def update_violation(request, violation_id):

    try:
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

        result = violations_collection.update_one(
            {"_id": ObjectId(violation_id)},
            {
                "$set": {
                    "vehicle_number": vehicle_number.upper(),
                    "owner_name": owner_name,
                    "violation_type": violation_type,
                    "location": location,
                    "officer_name": officer_name,
                    "fine_amount": int(fine_amount),
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

    except Exception as e:
        return Response(
            {"message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ==========================
# DELETE VIOLATION
# ==========================

@api_view(["DELETE"])
def delete_violation(request, violation_id):

    result = violations_collection.delete_one(

        {"_id": ObjectId(violation_id)}

    )

    if result.deleted_count == 0:

        return Response(

            {"message": "Violation Not Found"},

            status=status.HTTP_404_NOT_FOUND

        )

    return Response({

        "message": "Violation Deleted Successfully"

    })


# ==========================
# DASHBOARD STATISTICS
# ==========================

@api_view(["GET"])
def dashboard_statistics(request):

    total = violations_collection.count_documents({})

    paid = violations_collection.count_documents({

        "status": "Paid"

    })

    pending = violations_collection.count_documents({

        "status": "Pending"

    })

    total_fine = 0

    for violation in violations_collection.find():

        total_fine += violation.get("fine_amount", 0)

    return Response({

        "total_violations": total,

        "paid_violations": paid,

        "pending_violations": pending,

        "total_fine_amount": total_fine

    })