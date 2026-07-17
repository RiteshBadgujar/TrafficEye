from django.urls import path
from . import views

urlpatterns = [

    # GET ALL
    path("violations/", views.get_violations),

    # CREATE
    path("violations/create/", views.create_violation),

    # UPDATE
    path("violations/update/<str:violation_id>/", views.update_violation),

    # DELETE
    path("violations/delete/<str:violation_id>/", views.delete_violation),

    # GET SINGLE (KEEP THIS LAST)
    path("violations/<str:violation_id>/", views.get_violation),

    # DASHBOARD
    path("dashboard/", views.dashboard_statistics),

]