from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Users App
    path("", include("users.urls")),
    
    path("violations/", include("violations.urls")),
    
    path("reports/", include("reports.urls")),
    
    path("api/", include("api.urls")),

]