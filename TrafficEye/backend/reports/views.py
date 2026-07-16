from django.shortcuts import render
from database.mongodb import violations_collection
from datetime import datetime

def report_dashboard(request):

    total_violations = violations_collection.count_documents({})

    pending_fines = violations_collection.count_documents({
        "status": "Pending"
    })

    paid_fines = violations_collection.count_documents({
        "status": "Paid"
    })

    total_collection = 0

    paid_records = violations_collection.find({
        "status": "Paid"
    })

    for record in paid_records:
        total_collection += int(record["fine_amount"])

    context = {

        "total_violations": total_violations,
        "pending_fines": pending_fines,
        "paid_fines": paid_fines,
        "total_collection": total_collection

    }

    return render(
        request,
        "reports/report_dashboard.html",
        context
    )

# Daily Report
def daily_report(request):

    today = datetime.now().strftime("%d-%m-%Y")

    violations = list(
        violations_collection.find({
            "date": today
        })
    )

    total_collection = 0

    for violation in violations:

        violation["id"] = str(violation["_id"])

        if violation["status"] == "Paid":
            total_collection += int(violation["fine_amount"])

    context = {

        "today": today,
        "violations": violations,
        "total_collection": total_collection

    }

    return render(
        request,
        "reports/daily_report.html",
        context
    )

# Monthly Report
def monthly_report(request):

    current_month = datetime.now().strftime("%m-%Y")

    violations = list(violations_collection.find())

    monthly_violations = []
    total_collection = 0

    for violation in violations:

        # date format: dd-mm-yyyy
        month_year = "-".join(violation["date"].split("-")[1:])

        if month_year == current_month:

            violation["id"] = str(violation["_id"])
            monthly_violations.append(violation)

            if violation["status"] == "Paid":
                total_collection += int(violation["fine_amount"])

    context = {

        "month": current_month,
        "violations": monthly_violations,
        "total_collection": total_collection

    }

    return render(
        request,
        "reports/monthly_report.html",
        context
    )

# Yearly Report
def yearly_report(request):

    current_year = datetime.now().strftime("%Y")

    violations = list(violations_collection.find())

    yearly_data = []
    total_collection = 0

    for violation in violations:

        year = violation["date"].split("-")[2]

        if year == current_year:

            violation["id"] = str(violation["_id"])
            yearly_data.append(violation)

            if violation["status"] == "Paid":
                total_collection += int(violation["fine_amount"])

    return render(
        request,
        "reports/yearly_report.html",
        {
            "year": current_year,
            "violations": yearly_data,
            "total_collection": total_collection
        }
    )


# Vehicle Report
def vehicle_report(request):

    vehicle_number = request.GET.get("vehicle_number")

    violations = []

    if vehicle_number:

        violations = list(
            violations_collection.find(
                {
                    "vehicle_number": {
                        "$regex": vehicle_number.upper(),
                        "$options": "i"
                    }
                }
            )
        )

        for violation in violations:
            violation["id"] = str(violation["_id"])

    return render(
        request,
        "reports/vehicle_report.html",
        {
            "violations": violations
        }
    )


# Officer Report
def officer_report(request):

    officer_name = request.GET.get("officer_name")

    violations = []

    if officer_name:

        violations = list(
            violations_collection.find(
                {
                    "officer_name": {
                        "$regex": officer_name,
                        "$options": "i"
                    }
                }
            )
        )

        for violation in violations:
            violation["id"] = str(violation["_id"])

    return render(
        request,
        "reports/officer_report.html",
        {
            "violations": violations
        }
    )


# Pending Report
def pending_report(request):

    violations = list(
        violations_collection.find(
            {
                "status": "Pending"
            }
        )
    )

    for violation in violations:
        violation["id"] = str(violation["_id"])

    return render(
        request,
        "reports/pending_report.html",
        {
            "violations": violations
        }
    )


# Paid Report
def paid_report(request):

    violations = list(
        violations_collection.find(
            {
                "status": "Paid"
            }
        )
    )

    total_collection = 0

    for violation in violations:

        violation["id"] = str(violation["_id"])

        total_collection += int(violation["fine_amount"])

    return render(
        request,
        "reports/paid_report.html",
        {
            "violations": violations,
            "total_collection": total_collection
        }
    )