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
    """Authenticate a user and start a session."""
    if "user_id" in request.session:
        return redirect("dashboard")

    message = ""

    if request.method == "POST":

        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""

        user = get_user_by_email(email)

        if not user:
            message = "Email not found."

        elif not check_password(password, user["password"]):
            message = "Invalid Password."

        else:
            request.session["user_id"] = str(user["_id"])
            request.session["user_email"] = user["email"]
            request.session["user_name"] = user["full_name"]

            return redirect("dashboard")

    return render(
        request,
        "auth/login.html",
        {
            "message": message
        }
    )

# ==========================
# REGISTER USER
# ==========================

def register(request):
    """Register a new user account."""
    if "user_id" in request.session:
        return redirect("dashboard")

    message = ""

    if request.method == "POST":

        full_name = (request.POST.get("full_name") or "").strip()
        email = (request.POST.get("email") or "").strip().lower()
        mobile = (request.POST.get("mobile") or "").strip()
        password = request.POST.get("password") or ""
        confirm_password = request.POST.get("confirm_password") or ""

        # Validation
        if not full_name:
            message = "Full Name is required."

        elif not email:
            message = "Email is required."

        elif len(mobile) != 10 or not mobile.isdigit():
            message = "Enter a valid 10-digit mobile number."

        elif len(password) < 8:
            message = "Password must be at least 8 characters long."

        elif password != confirm_password:
            message = "Passwords do not match."

        elif get_user_by_email(email):
            message = "Email already registered."

        else:

            user = {
                "full_name": full_name,
                "email": email,
                "mobile": mobile,
                "password": make_password(password)
            }

            register_user(user)

            return redirect("login")

    return render(
        request,
        "auth/register.html",
        {
            "message": message
        }
    )
    
def dashboard(request):
    """Display dashboard statistics for the logged-in user."""
    
    if "user_id" not in request.session:
        return redirect("login")
    
    total_users = get_total_users()
    total_violations = get_total_violations()
    pending_fines = get_pending_fines()
    paid_fines = get_paid_fines()
    recent_violations = get_recent_violations()


    context = {

        "user_name": request.session.get("user_name"),

        "total_users": total_users,

        "total_violations": total_violations,

        "pending_fines": pending_fines,

        "paid_fines": paid_fines,

        "recent_violations": recent_violations

    }

    return render(request,
                  "dashboard/dashboard.html",
                    context)
    
# ==========================
# LOGOUT
# ==========================

def logout(request):
    
    """Authenticate a user and create a session."""
    if "user_id" not in request.session:
        return redirect("login")

    request.session.flush()

    return redirect("home")

# ==========================
# PROFILE
# ==========================

def profile(request):

    """Display the logged-in user's profile."""
        
    if "user_id" not in request.session:
        return redirect("login")

    context = {
        "user_name": request.session.get("user_name"),
        "user_email": request.session.get("user_email"),
    }

    return render(
        request,
        "profile.html",
        context
    )

# ==========================
# SETTINGS
# ==========================

def settings(request):
    """Display the user settings page."""
    
    if "user_id" not in request.session:
        return redirect("login")

    context = {
        "user_name": request.session.get("user_name"),
        "user_email": request.session.get("user_email"),
    }

    return render(
        request,
        "settings/settings.html",
        context
    )

# ==========================
# SEARCH VEHICLE
# ==========================

def search_vehicle(request):

    """Search for violations by vehicle number."""
    
    if "user_id" not in request.session:
        return redirect("login")

    violations = []

    if request.method == "POST":

        vehicle_no = (
            request.POST.get("vehicle_no") or ""
        ).strip().upper()

        if vehicle_no:
            violations = search_by_vehicle(vehicle_no)

    return render(
        request,
        "violations/search_vehicle.html",
        {
            "violations": violations
        }
    )