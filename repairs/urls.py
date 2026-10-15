from django.urls import path
from . import views

urlpatterns = [
    path("", views.maintenance_list, name="bookings"),
    path("<int:record_id>/", views.maintenance_detail, name="booking_detail"),
]
