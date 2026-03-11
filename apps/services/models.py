from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=40, blank=False)
    description = models.TextField(max_length=700, blank=False)
    image = models.ImageField(upload_to='services/', blank=False)

    def __str__(self):
        return self.title


# Create your models here.
