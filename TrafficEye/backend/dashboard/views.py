from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["trafficeye_db"]

violation_collection = db["violations"]


@login_required
def dashboard(request):

    total_violations = violation_collection.count_documents({})

    paid_cases = violation_collection.count_documents({
        "status": "Paid"
    })

    pending_cases = violation_collection.count_documents({
        "status": "Pending"
    })

    total_fine = 0

    for violation in violation_collection.find():

        total_fine += int(
            violation.get("fine_amount", 0)
        )

    recent_violations = violation_collection.find().sort(
        "_id",
        -1
    ).limit(5)

    context = {

        "total_violations": total_violations,

        "paid_cases": paid_cases,

        "pending_cases": pending_cases,

        "total_fine": total_fine,

        "recent_violations": recent_violations

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )