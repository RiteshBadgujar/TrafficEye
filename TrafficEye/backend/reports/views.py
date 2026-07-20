from django.shortcuts import redirect, render
from database.mongodb import violations_collection
from datetime import datetime
import csv
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def report_dashboard(request):
    
    if "user_id" not in request.session:
        return redirect("login")

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
    
    if "user_id" not in request.session:
        return redirect("login")

    today = datetime.now().strftime("%Y-%m-%d")

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

    if "user_id" not in request.session:
        return redirect("login")

    current_month = datetime.now().strftime("%m-%Y")

    violations = list(violations_collection.find())

    monthly_violations = []
    total_collection = 0

    for violation in violations:

        date_parts = violation["date"].split("-")

        if len(date_parts) == 3:

            month_year = f"{date_parts[1]}-{date_parts[0]}"

            if month_year == current_month:

                violation["id"] = str(violation["_id"])
                monthly_violations.append(violation)

                if violation["status"] == "Paid":
                    total_collection += int(violation["fine_amount"])

    return render(
        request,
        "reports/monthly_report.html",
        {
            "month": current_month,
            "violations": monthly_violations,
            "total_collection": total_collection
        }
    )

# Yearly Report
def yearly_report(request):

    if "user_id" not in request.session:
        return redirect("login")

    current_year = datetime.now().strftime("%Y")

    violations = list(violations_collection.find())

    yearly_data = []
    total_collection = 0

    for violation in violations:

        date_parts = violation["date"].split("-")

        if len(date_parts) == 3:

            year = date_parts[0]

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

    if "user_id" not in request.session:
        return redirect("login")

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

    if "user_id" not in request.session:
        return redirect("login")    

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

    if "user_id" not in request.session:
        return redirect("login")

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

    if "user_id" not in request.session:
        return redirect("login")

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
    
    # Export all violations to CSV
def export_csv(request):
    if "user_id" not in request.session:
        return redirect("login")

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = (
        'attachment; filename="traffic_violations.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Vehicle Number",
        "Owner Name",
        "Violation Type",
        "Officer Name",
        "Location",
        "Fine Amount",
        "Status",
        "Date"
    ])

    violations = violations_collection.find()

    for violation in violations:

        writer.writerow([
            violation.get("vehicle_number"),
            violation.get("owner_name"),
            violation.get("violation_type"),
            violation.get("officer_name"),
            violation.get("location"),
            violation.get("fine_amount"),
            violation.get("status"),
            violation.get("date")
        ])

    return response

def export_pdf(request):

    if "user_id" not in request.session:
        return redirect("login")

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        'attachment; filename="traffic_report.pdf"'
    )

    pdf = SimpleDocTemplate(response)

    data = [

        [
            "Vehicle",
            "Owner",
            "Violation",
            "Officer",
            "Fine",
            "Status",
            "Date"
        ]

    ]

    violations = violations_collection.find()

    for violation in violations:

        data.append([

            violation.get("vehicle_number"),

            violation.get("owner_name"),

            violation.get("violation_type"),

            violation.get("officer_name"),

            str(violation.get("fine_amount")),

            violation.get("status"),

            violation.get("date")

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.grey),

            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("BOTTOMPADDING", (0,0), (-1,0), 10)

        ])

    )

    pdf.build([table])

    return response