from django.urls import path
from .views import property_list

urlpatterns = [
    # This is mounted at /api/properties/ so we expose the list at the root
    path('', property_list, name='property-list'),
]
