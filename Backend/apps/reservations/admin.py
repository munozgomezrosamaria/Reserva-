
"""from django.contrib import admin
from apps.reservations.models import Reservation
# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("description", "state")
# Register your models here.
"""
from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('date', 'number_persons', 'state', 'user', 'create_at')

admin.site.register(Reservation, ReservationAdmin)