from django.shortcuts import render, redirect
from datetime import datetime
import csv
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from database.violation_service import (
    add_violation as add_violation_service,
    get_violation_by_id,
    update_violation as update_violation_service,
    delete_violation as delete_violation_service,
    get_filtered_violations,
    count_filtered_violations,
    mark_fine_paid as mark_fine_paid_service,
)


def _safe_int(value, default=0):
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_upper(value):
    value = (value or "").strip()
    return value.upper() if value else ""


def _build_query(search, status, violation_type):
    query = {}

    if search:
        query["$or"] = [
            {
                "vehicle_number": {"$regex": search, "$options": "i"}
            },
            {
                "owner_name": {"$regex": search, "$options": "i"}
            },
        ]

    if status:
        query["status"] = status

    if violation_type:
        query["violation_type"] = violation_type

    return query

# Add new violation
def add_violation(request):
    
    if "user_id" not in request.session:
        return redirect("login")

    if request.method == "POST":
        # Read form fields
        vehicle_number = request.POST.get("vehicle_number", "").strip().upper()
        owner_name = request.POST.get("owner_name", "").strip()
        violation_type = request.POST.get("violation_type", "").strip()
        location = request.POST.get("location", "").strip()
        officer_name = request.POST.get("officer_name", "").strip()

        # Parse fine amount
        fine = request.POST.get("fine_amount", "0")
        try:
            fine = int(fine)
        except (TypeError, ValueError):
            fine = 0

        violation = {
            "vehicle_number": vehicle_number,
            "owner_name": owner_name,
            "violation_type": violation_type,
            "location": location,
            "fine_amount": fine,
            "officer_name": officer_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Pending"
        }

        add_violation_service(violation)

        return redirect("violation_list")

    return render(request, "violations/add_violation.html")


# Display all violations with Search, Filter, Sorting and Pagination
def violation_list(request):

    if "user_id" not in request.session:
        return redirect("login")

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    violation_type = request.GET.get("type", "").strip()
    sort = request.GET.get("sort", "newest")
    page_number = request.GET.get("page", 1)

    query = _build_query(search, status, violation_type)

    cursor = get_filtered_violations(query, sort)

    total = count_filtered_violations(query)

    paginator = Paginator(range(total), 10)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    per_page = paginator.per_page
    skip = (current_page - 1) * per_page

    violations = list(
        cursor.skip(skip).limit(per_page)
    )

    for violation in violations:
        violation["id"] = str(violation["_id"])

    page_obj.object_list = violations  # type: ignore

    return render(
        request,
        "violations/violations_list.html",
        {
            "page_obj": page_obj,
            "search": search,
            "status": status,
            "violation_type": violation_type,
            "sort": sort,
        },
    )

# Search by vehicle number
# NOTE: This functionality is intentionally not duplicated here.
# The main violation_list view already provides search by vehicle number/owner.
# Keeping this function would lead to two different search behaviors.
# If needed later, it can be re-enabled.



# ==========================
# EDIT VIOLATION
# ==========================

def edit_violation(request, violation_id):

    if "user_id" not in request.session:
        return redirect("login")

    violation = get_violation_by_id(violation_id)

    if not violation:
        return redirect("violation_list")

    violation["id"] = str(violation["_id"])

    if request.method == "POST":

        vehicle_number = _safe_upper(
            request.POST.get("vehicle_number")
        )

        owner_name = (
            request.POST.get("owner_name") or ""
        ).strip()

        violation_type = (
            request.POST.get("violation_type") or ""
        ).strip()

        location = (
            request.POST.get("location") or ""
        ).strip()

        officer_name = (
            request.POST.get("officer_name") or ""
        ).strip()

        fine_amount = _safe_int(
            request.POST.get("fine_amount"),
            default=0
        )

        status_value = (
            request.POST.get("status") or "Pending"
        ).strip()

        # Validation
        if not vehicle_number:
            return render(
                request,
                "violations/edit_violation.html",
                {
                    "violation": violation,
                    "error": "Vehicle Number is required."
                }
            )

        update_payload = {
            "vehicle_number": vehicle_number,
            "owner_name": owner_name,
            "violation_type": violation_type,
            "location": location,
            "fine_amount": fine_amount,
            "officer_name": officer_name,
            "status": status_value,
        }

        date_str = request.POST.get("date")

        if date_str:
            update_payload["date"] = date_str

        update_violation_service(
            violation_id,
            update_payload
        )

        return redirect("violation_list")

    return render(
        request,
        "violations/edit_violation.html",
        {
            "violation": violation
        }
    )
# ==========================
# DELETE VIOLATION
# ==========================

def delete_violation(request, violation_id):

    if "user_id" not in request.session:
        return redirect("login")

    violation = get_violation_by_id(violation_id)

    if not violation:
        return redirect("violation_list")

    if request.method == "POST":

        delete_violation_service(violation_id)

        return redirect("violation_list")

    return render(
        request,
        "violations/delete_violation.html",
        {
            "violation": violation
        }
    )
# Export Violations to CSV

# ==========================
# EXPORT VIOLATIONS TO CSV
# ==========================

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
        "Location",
        "Fine Amount",
        "Officer Name",
        "Date",
        "Status",
    ])

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    violation_type = request.GET.get("type", "").strip()
    sort = request.GET.get("sort", "newest")

    query = _build_query(search, status, violation_type)

    violations = get_filtered_violations(query, sort)

    for violation in violations:

        writer.writerow([
            violation.get("vehicle_number", ""),
            violation.get("owner_name", ""),
            violation.get("violation_type", ""),
            violation.get("location", ""),
            violation.get("fine_amount", 0),
            violation.get("officer_name", ""),
            violation.get("date", ""),
            violation.get("status", ""),
        ])

    return response

# ==========================
# EXPORT VIOLATIONS TO PDF
# ==========================

def export_pdf(request):

    if "user_id" not in request.session:
        return redirect("login")

    return HttpResponse(
        "PDF Export Coming Soon...",
        content_type="text/plain"
    )


def pay_fine(request, violation_id):

    if "user_id" not in request.session:
        return redirect("login")

    if request.method == "POST":
        mark_fine_paid_service(violation_id)
        messages.success(request, "Fine marked as paid successfully.")
        return redirect("violation_list")

    violation = get_violation_by_id(violation_id)

    if not violation:
        return redirect("violation_list")

    violation["id"] = str(violation["_id"])

    return render(
        request,
        "violations/pay_fine.html",
        {
            "violation": violation
        }
    )