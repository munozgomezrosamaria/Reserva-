from django.urls import path
from .api_views import ServiceListAPIView, ServiceDetailAPIView

urlpatterns = [
    path('', ServiceListAPIView.as_view(), name='api_services_list'),
    path('<int:pk>/', ServiceDetailAPIView.as_view(), name='api_service_detail'),
]
