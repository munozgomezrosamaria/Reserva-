from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=40, blank=False)
    description = models.TextField(max_length=700, blank=False)
    image = models.CharField(max_length=500, null=True, blank=True, help_text="Ruta de Vercel (ej: /images/servicio1.jpg)")

    def __str__(self):
        return self.title


# Create your models here.
