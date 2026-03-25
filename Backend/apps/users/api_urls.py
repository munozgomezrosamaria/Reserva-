from django.urls import path
from .api_views import RegisterAPIView, UserProfileAPIView, AdminUserListAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('profile/', UserProfileAPIView.as_view(), name='api_profile'),
    path('admin/', AdminUserListAPIView.as_view(), name='api_admin_users'),
]