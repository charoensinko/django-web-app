from django.urls import path
from . import views

app_name = "training"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.training_add, name="add"),
    path("<int:pk>/edit/", views.training_edit, name="edit"),
    path("<int:pk>/delete/", views.training_delete, name="delete"),
]
