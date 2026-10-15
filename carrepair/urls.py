from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("vehicles/", include("cars.urls")),
    path("cars/", include("cars.urls")),
    path("maintenance/", include("repairs.urls")),
    path("repairs/", include("repairs.urls")),
    path("bookings/", include("repairs.urls")),
]

handler404 = "homepage.views.page_not_found"
