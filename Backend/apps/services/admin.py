from django.contrib import admin
from apps.services.models import Service
# Register your models here.
@admin.register(Service)
class ServiceAdminAdmin(admin.ModelAdmin):
    list_display = ("title","description")


