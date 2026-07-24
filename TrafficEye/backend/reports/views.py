from django.shortcuts import redirect, render
from datetime import datetime
import csv
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from database.violation_service import (
    get_all_violations,
    get_total_violations,
    get_pending_fines,
    get_paid_fines,
    get_total_collection,
    search_vehicle_report,
    search_officer_report,
    get_pending_violations,
    get_paid_violations,
    get_daily_report
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)
def report_dashboard(request):
    
    if "user_id" not in request.session:
        return redirect("login")

    total_violations = get_total_violations()

    pending_fines = get_pending_fines()

    paid_fines = get_paid_fines()

    total_collection = get_total_collection()

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

    violations = get_daily_report(today)

    total_collection = 0

    for violation in violations:

        violation["id"] = str(violation["_id"])

        if violation.get("status") == "Paid":
            total_collection += int(
                violation.get("fine_amount", 0)
)
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

    violations = get_all_violations()

    monthly_violations = []
    total_collection = 0

    for violation in violations:

        date_parts = violation.get("date", "").split("-")

        if len(date_parts) == 3:

            month_year = f"{date_parts[1]}-{date_parts[0]}"

            if month_year == current_month:

                violation["id"] = str(violation["_id"])
                monthly_violations.append(violation)

                if violation.get("status") == "Paid":
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

    violations = get_all_violations()

    yearly_data = []
    total_collection = 0

    for violation in violations:

        date_parts = violation.get("date", "").split("-")

        if len(date_parts) == 3:

            year = date_parts[0]

            if year == current_year:

                violation["id"] = str(violation["_id"])
                yearly_data.append(violation)

                if violation.get("status") == "Paid":
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

    vehicle_number = (
        request.GET.get("vehicle_number") or ""
    ).strip().upper()

    violations = []

    if vehicle_number:

        violations = search_vehicle_report(vehicle_number)

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

    officer_name = (
        request.GET.get("officer_name") or ""
    ).strip()
    
    violations = []

    if officer_name:

        violations = search_officer_report(officer_name)

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

    violations = get_pending_violations()

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

    violations = get_paid_violations()

    total_collection = 0

    for violation in violations:

        violation["id"] = str(violation["_id"])

        total_collection += int(
            violation.get("fine_amount", 0)
    )

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

    violations = get_all_violations()

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

    pdf = SimpleDocTemplate(response)  # type: ignore[arg-type]

    # Table Header
    data = [[
        "Vehicle",
        "Owner",
        "Violation",
        "Officer",
        "Fine",
        "Status",
        "Date"
    ]]

    # Fetch all violations
    violations = get_all_violations()

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

    # Create table
    table = Table(
        data,
        colWidths=[80, 80, 90, 80, 50, 60, 70]
    )

    # Table Style
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ])
    )

    # PDF Content
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("<b>TrafficEye</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Traffic Violation Report", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y')}",
            styles["Normal"]
        )
    )

    elements.append(table)

    elements.append(
        Paragraph(
            f"<br/><b>Total Violations:</b> {len(data) - 1}",
            styles["Normal"]
        )
    )

    pdf.build(elements)

    return response