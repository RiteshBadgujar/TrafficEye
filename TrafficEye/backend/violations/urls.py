from django.urls import path
from . import views

urlpatterns = [

    path("add/", views.add_violation, name="add_violation"),

    path("list/", views.violation_list, name="violation_list"),

    path("search/", views.search_violation, name="search_violation"),

    path("edit/<str:violation_id>/",
         views.edit_violation,
         name="edit_violation"),

    path("delete/<str:violation_id>/",
         views.delete_violation,
         name="delete_violation"),
    
    path(
    "pay/<str:violation_id>/",
    views.pay_fine,
    name="pay_fine"
),

]