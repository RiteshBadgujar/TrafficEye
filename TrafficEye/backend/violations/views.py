from django.shortcuts import render, redirect
from database.mongodb import violations_collection
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
import csv
from django.http import HttpResponse
from django.core.paginator import Paginator



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


def _apply_sort(cursor, sort):
    if sort == "oldest":
        return cursor.sort("date", 1)
    return cursor.sort("date", -1)


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

        violations_collection.insert_one(violation)

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

    page_number = request.GET.get("page")

    query = _build_query(search, status, violation_type)

    cursor = _apply_sort(violations_collection.find(query), sort)

    # Convert only the current page slice to Python objects
    total = violations_collection.count_documents(query)
    paginator = Paginator(range(total), 10)
    page_obj = paginator.get_page(page_number)

    # Paginator uses 1-based indices for page numbers; compute 0-based skip
    current_page = page_obj.number
    per_page = paginator.per_page
    skip = (current_page - 1) * per_page

    violations = list(cursor.skip(skip).limit(per_page))

    for violation in violations:
        violation["id"] = str(violation["_id"])

    # Rebuild a lightweight Page-like object expected by template
    page_obj = paginator.get_page(current_page)
    page_obj.object_list = violations

    return render(

        request,

        "violations/violations_list.html",

        {

            "page_obj": page_obj,

            "search": search,

            "status": status,

            "violation_type": violation_type,

            "sort": sort

        }

    )

# Search by vehicle number
# NOTE: This functionality is intentionally not duplicated here.
# The main violation_list view already provides search by vehicle number/owner.
# Keeping this function would lead to two different search behaviors.
# If needed later, it can be re-enabled.



# Edit violation
def edit_violation(request, violation_id):

    if "user_id" not in request.session:
        return redirect("login")
    
    try:
        obj_id = ObjectId(violation_id)
    except (TypeError, ValueError, InvalidId):
        return redirect("violation_list")

    violation = violations_collection.find_one({"_id": obj_id})

    if violation:
        violation["id"] = str(violation["_id"])

    if request.method == "POST":

        vehicle_number = request.POST.get("vehicle_number")
        vehicle_number = _safe_upper(vehicle_number)

        officer_name = (request.POST.get("officer_name") or "").strip()
        if not officer_name:
            officer_name = violation.get("officer_name", "") if violation else ""

        fine_amount = _safe_int(request.POST.get("fine_amount"), default=0)

        update_payload = {
            "vehicle_number": vehicle_number,
            "owner_name": (request.POST.get("owner_name") or "").strip(),
            "violation_type": (request.POST.get("violation_type") or "").strip(),
            "location": (request.POST.get("location") or "").strip(),
            "fine_amount": fine_amount,
            "officer_name": officer_name,
            "status": (request.POST.get("status") or "Pending").strip(),
        }

        # Preserve existing date format; allow editing date if provided.
        date_str = request.POST.get("date")
        if date_str:
            update_payload["date"] = str(date_str)

        violations_collection.update_one(
            {"_id": obj_id},
            {"$set": update_payload}
        )

        return redirect("violation_list")

    return render(
        request,
        "violations/edit_violation.html",
        {"violation": violation}
    )


# Delete violation
def delete_violation(request, violation_id):
    
    if "user_id" not in request.session:
        return redirect("login")

    if request.method != "POST":
        return redirect("violation_list")

    try:
        obj_id = ObjectId(violation_id)
    except (TypeError, ValueError, InvalidId):
        return redirect("violation_list")

    violations_collection.delete_one({"_id": obj_id})

    return redirect("violation_list")


# Mark violation as paid
def pay_fine(request, violation_id):
    
    if "user_id" not in request.session:
        return redirect("login")

    try:
        obj_id = ObjectId(violation_id)
    except (TypeError, ValueError, InvalidId):
        return redirect("violation_list")

    violations_collection.update_one(
        {"_id": obj_id},
        {"$set": {"status": "Paid"}}
    )

    return redirect("violation_list")
# Export Violations to CSV

def export_csv(request):
    
    if "user_id" not in request.session:
        return redirect("login")

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="traffic_violations.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Vehicle Number",
        "Owner Name",
        "Violation Type",
        "Location",
        "Fine Amount",
        "Officer Name",
        "Date",
        "Status"
    ])

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    violation_type = request.GET.get("type", "").strip()
    sort = request.GET.get("sort", "newest")

    query = _build_query(search, status, violation_type)

    cursor = _apply_sort(violations_collection.find(query), sort)

    for violation in cursor:

        writer.writerow([

            violation.get("vehicle_number"),

            violation.get("owner_name"),

            violation.get("violation_type"),

            violation.get("location"),

            violation.get("fine_amount"),

            violation.get("officer_name"),

            violation.get("date"),

            violation.get("status")

        ])

    return response

def export_pdf(request):
    
    if "user_id" not in request.session:
        return redirect("login")
    return HttpResponse("PDF Export Coming Soon")

