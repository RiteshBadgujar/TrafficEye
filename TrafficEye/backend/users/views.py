from django.shortcuts import render

def home(request):
    """
    Home Page
    """
    return render(request, "home.html")