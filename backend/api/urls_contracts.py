from django.urls import path
from .views_contracts import (
    RegisterPropertyView, CreateLeaseView, PayRentView, DepositSavingsView, PayOnBehalfView, UpdateReputationView
)

urlpatterns = [
    path('property/register', RegisterPropertyView.as_view()),
    path('lease/create', CreateLeaseView.as_view()),
    path('rent/<int:lease_id>/pay', PayRentView.as_view()),
    path('savings/<int:plan_id>/deposit', DepositSavingsView.as_view()),
    path('thirdparty/pay', PayOnBehalfView.as_view()),
    path('reputation/<str:user>/<str:action>', UpdateReputationView.as_view()),
]
