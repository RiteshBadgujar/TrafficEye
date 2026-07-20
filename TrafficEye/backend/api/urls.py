from django.urls import path
from . import views

urlpatterns = [
    # API Home
    path("", views.api_home, name="api_home"),

    # Dashboard
    path("dashboard/", views.dashboard_statistics, name="dashboard_statistics"),

    # Violations
    path("violations/", views.get_violations, name="get_violations"),
    path("violations/<str:violation_id>/", views.get_violation, name="get_violation"),
    path("violations/create/", views.create_violation, name="create_violation"),
    path("violations/update/<str:violation_id>/", views.update_violation, name="update_violation"),
    path("violations/delete/<str:violation_id>/", views.delete_violation, name="delete_violation"),
]