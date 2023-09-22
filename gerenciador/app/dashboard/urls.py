from django.urls import path
from .views import *


app_name = "app.dashboard"

urlpatterns = [
    path(
        "",
        dashboard,
        name="dashboard",
    ),
]
