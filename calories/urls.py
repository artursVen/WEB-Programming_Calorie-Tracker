from django.urls import path

from . import views


app_name = "calories"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
