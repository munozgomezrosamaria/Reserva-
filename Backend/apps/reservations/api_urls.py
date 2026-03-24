from django.urls import path
from .api_views import ReservationListCreateAPIView, ReservationDetailAPIView

urlpatterns = [
    path('', ReservationListCreateAPIView.as_view(), name='api_reservations_list'),
    path('<int:pk>/', ReservationDetailAPIView.as_view(), name='api_reservation_detail'),
]
