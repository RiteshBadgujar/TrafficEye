from django.urls import path
from . import views

urlpatterns = [

    path("", views.report_dashboard, name="report_dashboard"),

    path("daily/", views.daily_report, name="daily_report"),

    path("monthly/", views.monthly_report, name="monthly_report"),

    path("yearly/", views.yearly_report, name="yearly_report"),

    path("vehicle/", views.vehicle_report, name="vehicle_report"),

    path("officer/", views.officer_report, name="officer_report"),

    path("pending/", views.pending_report, name="pending_report"),

    path("paid/", views.paid_report, name="paid_report"),

]