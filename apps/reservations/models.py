from django.db import models
from apps.services.models import Service
from django.conf import settings

class Reservation(models.Model):
    STATES = [
        ("confirmado", "Confirmado"),
        ("pendiente", "Pendiente"),
        ("cancelado", "Cancelado"),
    ]
    date = models.DateField(blank=False)
    number_persons = models.PositiveIntegerField(blank=False)
    state = models.CharField(max_length=20, blank=False, choices=STATES, default="pendiente")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reservations")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.user} - {self.service}"

