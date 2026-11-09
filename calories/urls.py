from django.urls import path

from . import views

app_name = "calories"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "entries/<int:entry_id>/edit/",
        views.edit_food_entry,
        name="edit_entry",
    ),
    path(
        "entries/<int:entry_id>/delete/",
        views.delete_food_entry,
        name="delete_entry",
    ),
]
