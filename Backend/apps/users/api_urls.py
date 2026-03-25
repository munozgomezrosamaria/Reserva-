from django.urls import path
from .api_views import RegisterAPIView, UserProfileAPIView, PasswordResetRequestAPIView, PasswordResetConfirmAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('profile/', UserProfileAPIView.as_view(), name='api_profile'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='api_password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm'),
]
