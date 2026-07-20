from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from database.user_service import (
    register_user,
    get_user_by_email,
    get_total_users,
)

from database.violation_service import (
    get_total_violations,
    get_pending_fines,
    get_paid_fines,
    get_recent_violations,
    search_by_vehicle,
)

def home(request):
    return render(request, "home/home.html")


def login(request):

    message = ""

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = get_user_by_email(email)
        if user:

            if check_password(password, user["password"]):
                
                request.session["user_id"] = str(user["_id"])
                request.session["user_email"] = user["email"]
                request.session["user_name"] = user["full_name"]

                return redirect("dashboard")

            else:
                message = "Invalid Password."

        else:
            message = "Email not found."

    return render(request, "auth/login.html", {"message": message})


def register(request):

    message = ""

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not full_name:
            message = "Full Name is required."

        elif not email:
            message = "Email is required."

        elif len(mobile) != 10 or not mobile.isdigit():
            message = "Enter a valid 10-digit mobile number."

        elif password != confirm_password:
            message = "Passwords do not match."

        else:

            existing_user = get_user_by_email(email)

            if existing_user:
                message = "Email already registered."

            else:

                user = {
                    "full_name": full_name,
                    "email": email,
                    "mobile": mobile,
                    "password": make_password(password)
                }

                register_user(user)

                message = "Registration Successful!"

    return render(request, "auth/register.html", {"message": message})

def dashboard(request):

    if "user_email" not in request.session:
        return redirect("login")
    
    total_users = get_total_users()
    total_violations = get_total_violations()
    pending_fines = get_pending_fines()
    paid_fines = get_paid_fines()
    recent_violations = get_recent_violations()


    context = {

        "user_name": request.session["user_name"],

        "total_users": total_users,

        "total_violations": total_violations,

        "pending_fines": pending_fines,

        "paid_fines": paid_fines,

        "recent_violations": recent_violations

    }

    return render(request,
                  "dashboard/dashboard.html",
                    context)
    
def logout(request):

    if "user_email" not in request.session:
        return redirect("login")

    request.session.flush()

    return redirect("home")

def profile(request):

    if "user_email" not in request.session:
        return redirect("login")

    context = {
        "user_name": request.session["user_name"],
        "user_email": request.session["user_email"],
    }

    return render(request, "profile.html", context)

def settings(request):

    if "user_email" not in request.session:
        return redirect("login")

    context = {
        "user_name": request.session["user_name"],
        "user_email": request.session["user_email"],
    }

    return render(request, "settings/settings.html", context)


def search_vehicle(request):

    if "user_email" not in request.session:
        return redirect("login")

    violations = []

    if request.method == "POST":
        vehicle_no = request.POST.get("vehicle_no")
        violations = search_by_vehicle(vehicle_no)

    return render(
        request,
        "violations/search_vehicle.html",
        {
            "violations": violations
        }
    )