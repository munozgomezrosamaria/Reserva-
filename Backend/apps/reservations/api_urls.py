from django.urls import path
from .api_views import (
    ReservationListCreateAPIView,
    ReservationDetailAPIView,
    AdminReservationListAPIView,
    AdminReservationDetailAPIView
)

urlpatterns = [
    path('', ReservationListCreateAPIView.as_view(), name='api_reservations_list'),
    path('<int:pk>/', ReservationDetailAPIView.as_view(), name='api_reservation_detail'),
    path('admin/', AdminReservationListAPIView.as_view(), name='api_admin_reservations'),
    path('admin/<int:pk>/', AdminReservationDetailAPIView.as_view(), name='api_admin_reservation_detail'),
]