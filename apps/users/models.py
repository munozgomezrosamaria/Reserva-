import uuid

from django.db import models

'-----------------Tabla de usuarios-----------------'
class User(models.Model):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    referencia = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.username
    

'-----------------Tabla de servicios-----------------'    
class servicio(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    referencia = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    

    def __str__(self):
        return self.name
    
    
'-----------------Tabla de reservas-----------------'
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    servicio = models.ForeignKey('servicio', on_delete=models.CASCADE,related_name='reservations')

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.date} at {self.time}"


