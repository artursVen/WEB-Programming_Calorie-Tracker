from django.urls import path

from . import views


app_name = "calories"

urlpatterns = [
    path("", views.dashborad, name="dashboard"),
]
