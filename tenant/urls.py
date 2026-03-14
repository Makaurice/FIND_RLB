from django.urls import path

from tenant.views import (
    TenantProfileAPIView,
    LeaseListCreateAPIView,
    PaymentListCreateAPIView,
    ReviewListCreateAPIView,
    TenantTrustScoreAPIView,
)

app_name = 'tenant'

urlpatterns = [
    path('profile/', TenantProfileAPIView.as_view(), name='tenant-profile'),
    path('leases/', LeaseListCreateAPIView.as_view(), name='tenant-leases'),
    path('payments/', PaymentListCreateAPIView.as_view(), name='tenant-payments'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='tenant-reviews'),
    path('trust-score/', TenantTrustScoreAPIView.as_view(), name='tenant-trust-score'),
]
