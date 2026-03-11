from django.shortcuts import render
from .models import Service

def Services(request):
    services = Service.objects.all()
    return render(request, "presentations/services.html", {"services": services})
