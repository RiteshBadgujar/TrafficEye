from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_violation, name="add_violation"),
    path("list/", views.violation_list, name="violation_list"),
    path( "search/", views.search_violation, name="search_violation"),
]
