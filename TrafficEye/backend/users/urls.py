from django.urls import path
from . import views

urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Authentication
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # User
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),

    # Search
    path("search/", views.search_vehicle, name="search_vehicle"),
]