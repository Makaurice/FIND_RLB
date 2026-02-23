from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshTokenAPIView,
    VerifyTokenAPIView,
    ProfileAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='token-refresh'),
    path('verify/', VerifyTokenAPIView.as_view(), name='verify-token'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
