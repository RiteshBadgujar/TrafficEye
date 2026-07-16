from django.shortcuts import render, redirect
from database.mongodb import violations_collection
from datetime import datetime


def add_violation(request):

    message = ""

    if request.method == "POST":

        vehicle_number = request.POST.get("vehicle_number")
        owner_name = request.POST.get("owner_name")
        violation_type = request.POST.get("violation_type")
        location = request.POST.get("location")
        fine_amount = request.POST.get("fine_amount")
        officer_name = request.POST.get("officer_name")

        violation = {
            "vehicle_number": vehicle_number.upper(),
            "owner_name": owner_name,
            "violation_type": violation_type,
            "location": location,
            "fine_amount": int(fine_amount),
            "officer_name": officer_name,
            "date": datetime.now().strftime("%d-%m-%Y"),
            "status": "Pending"
        }

        violations_collection.insert_one(violation)

        return redirect("violation_list")

    return render(request, "violations/add_violation.html")


def violation_list(request):

    violations = violations_collection.find()

    return render(request,
                  "violations/violations_list.html",
                  {"violations": violations})
def search_violation(request):

    violations = []

    if request.method == "GET":

        vehicle_number = request.GET.get("vehicle_number")

        if vehicle_number:

            violations = violations_collection.find({
                "vehicle_number": {
                    "$regex": vehicle_number.upper(),
                    "$options": "i"
                }
            })

    return render(
        request,
        "violations/search_violation.html",
        {"violations": violations}
    )