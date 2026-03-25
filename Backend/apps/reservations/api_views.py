from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReservationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class AdminReservationListAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        return Reservation.objects.select_related('user', 'service').all().order_by('-created_at')

class AdminReservationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]
    queryset = Reservation.objects.all()