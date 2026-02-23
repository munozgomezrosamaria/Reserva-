from django.contrib import admin

from .models import User, servicio, Reservation

admin.site.register(User)
admin.site.register(servicio)
admin.site.register(Reservation)
