from django.urls import path
from . import views
from . import api_views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "chart-data/",
        api_views.chart_data,
        name="chart_data"
    ),

]