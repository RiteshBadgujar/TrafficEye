from django.urls import path
from . import views

urlpatterns = [

    path("", views.violation_list, name="violation_list"),

    path("add/", views.add_violation, name="add_violation"),

    path("edit/<str:violation_id>/", views.edit_violation, name="edit_violation"),

    path("delete/<str:violation_id>/", views.delete_violation, name="delete_violation"),

    path("pay/<str:violation_id>/", views.pay_fine, name="pay_fine"),

    path("export/csv/", views.export_csv, name="export_csv"),
    
    path( "export/pdf/", views.export_pdf, name="export_pdf"),

]