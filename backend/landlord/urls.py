from django.urls import path
from .views import (
    PropertyListingsAPI,
    PricingSettingsAPI,
    PaymentScheduleAPI,
    RentHistoryAPI,
    AnalyticsAPI
)

urlpatterns = [
    path('listings/', PropertyListingsAPI.as_view(), name='property-listings'),
    path('pricing/', PricingSettingsAPI.as_view(), name='pricing-settings'),
    path('schedules/', PaymentScheduleAPI.as_view(), name='payment-schedules'),
    path('history/', RentHistoryAPI.as_view(), name='rent-history'),
    path('analytics/', AnalyticsAPI.as_view(), name='analytics'),
]
