from django.urls import path
from .views import (
    MoversServicesAPI,
    MovingBookingsAPI,
    MaintenanceRequestsAPI,
    StorageUnitsAPI,
    InventoryAPI
)

urlpatterns = [
    path('movers/', MoversServicesAPI.as_view(), name='movers-services'),
    path('bookings/', MovingBookingsAPI.as_view(), name='moving-bookings'),
    path('maintenance/', MaintenanceRequestsAPI.as_view(), name='maintenance-requests'),
    path('storage/', StorageUnitsAPI.as_view(), name='storage-units'),
    path('inventory/', InventoryAPI.as_view(), name='inventory'),
]
