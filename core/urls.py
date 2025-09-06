from django.urls import path
from . import views  # import views from the same app

urlpatterns = [
    path("", views.index, name="index"),
]
