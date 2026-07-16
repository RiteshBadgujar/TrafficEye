from django.shortcuts import render, redirect
from database.mongodb import violations_collection
from datetime import datetime
from bson import ObjectId


# Add new violation
def add_violation(request):

    if request.method == "POST":

        violation = {
            "vehicle_number": request.POST.get("vehicle_number").upper(),
            "owner_name": request.POST.get("owner_name"),
            "violation_type": request.POST.get("violation_type"),
            "location": request.POST.get("location"),
            "fine_amount": int(request.POST.get("fine_amount")),
            "officer_name": request.POST.get("officer_name"),
            "date": datetime.now().strftime("%d-%m-%Y"),
            "status": "Pending"
        }

        violations_collection.insert_one(violation)

        return redirect("violation_list")

    return render(request, "violations/add_violation.html")


# Display all violations
def violation_list(request):

    violations = list(violations_collection.find())

    # Convert MongoDB _id to normal id
    for violation in violations:
        violation["id"] = str(violation["_id"])

    return render(
        request,
        "violations/violations_list.html",
        {"violations": violations}
    )


# Search by vehicle number
def search_violation(request):

    violations = []

    vehicle_number = request.GET.get("vehicle_number")

    if vehicle_number:

        violations = list(
            violations_collection.find({
                "vehicle_number": {
                    "$regex": vehicle_number.upper(),
                    "$options": "i"
                }
            })
        )

        for violation in violations:
            violation["id"] = str(violation["_id"])

    return render(
        request,
        "violations/search_violation.html",
        {"violations": violations}
    )


# Edit violation
def edit_violation(request, violation_id):

    violation = violations_collection.find_one(
        {"_id": ObjectId(violation_id)}
    )

    if violation:
        violation["id"] = str(violation["_id"])

    if request.method == "POST":

        violations_collection.update_one(

            {"_id": ObjectId(violation_id)},

            {
                "$set": {

                    "vehicle_number": request.POST.get("vehicle_number").upper(),
                    "owner_name": request.POST.get("owner_name"),
                    "violation_type": request.POST.get("violation_type"),
                    "location": request.POST.get("location"),
                    "fine_amount": int(request.POST.get("fine_amount")),
                    "officer_name": request.POST.get("officer_name"),
                    "status": request.POST.get("status")

                }
            }

        )

        return redirect("violation_list")

    return render(
        request,
        "violations/edit_violation.html",
        {"violation": violation}
    )


# Delete violation
def delete_violation(request, violation_id):

    violations_collection.delete_one(
        {"_id": ObjectId(violation_id)}
    )

    return redirect("violation_list")

# Mark violation as paid
def pay_fine(request, violation_id):

    violations_collection.update_one(
        {"_id": ObjectId(violation_id)},
        {
            "$set": {
                "status": "Paid"
            }
        }
    )

    return redirect("violation_list")