from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    # Django Admin
    path("admin/", admin.site.urls),

    # User Management
    path("", include("users.urls")),

    # Traffic Violations
    path("violations/", include("violations.urls")),

    # Reports
    path("reports/", include("reports.urls")),

    # REST API
    path("api/", include("api.urls")),

]