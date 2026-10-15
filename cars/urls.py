from django.urls import path
from . import views

urlpatterns = [
    path("", views.vehicles_list, name="vehicles"),
    path("<int:vehicle_id>/", views.vehicle_detail, name="room_detail"),
]
