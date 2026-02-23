from django.urls import path
from .views import TenantList

urlpatterns = [
    path('tenants/', TenantList.as_view(), name='tenant-list'),
]
