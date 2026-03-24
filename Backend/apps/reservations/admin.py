from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('date', 'number_persons', 'state', 'user', 'created_at')

admin.site.register(Reservation, ReservationAdmin)