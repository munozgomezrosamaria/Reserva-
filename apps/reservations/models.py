from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Service

class Reservation(models.Model):
    states = [("confirmado","Confirmado"),("pendiente", "Pendiente"),("eliminar", "Eliminar")]
    date = models.DateField(blank=False)
    number_persons = models.PositiveIntegerField(blank=False)
    state = models.CharField(blank=False,choices = states)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "reservations")
    user = models.ForeignKey(Service, on_delete=models.CASCADE, related_name= "reservations")
    create_at = models.DateTimeField (auto_now_add=True)

    def __str__(self):
        return self.name

