from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from database.mongodb import users_collection


def home(request):
    return render(request, "home/home.html")


def login(request):

    message = ""

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = users_collection.find_one({"email": email})

        if user:

            if check_password(password, user["password"]):

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

            existing_user = users_collection.find_one({"email": email})

            if existing_user:
                message = "Email already registered."

            else:

                user = {
                    "full_name": full_name,
                    "email": email,
                    "mobile": mobile,
                    "password": make_password(password)
                }

                users_collection.insert_one(user)

                message = "Registration Successful!"

    return render(request, "auth/register.html", {"message": message})


def dashboard(request):

    if "user_email" not in request.session:
        return redirect("login")

    return render(request, "dashboard/dashboard.html")


def logout(request):

    request.session.flush()

    return redirect("home")