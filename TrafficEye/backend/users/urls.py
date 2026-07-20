from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("search/", views.search_vehicle, name="search_vehicle"),
    
]
    