from django.urls import path
from .views import TenantProfileView, LeaseListCreateView, PaymentListCreateView

urlpatterns = [
    path('tenant/profile/', TenantProfileView.as_view(), name='tenant-profile'),
    path('tenant/leases/', LeaseListCreateView.as_view(), name='tenant-leases'),
    path('tenant/payments/', PaymentListCreateView.as_view(), name='tenant-payments'),
]
