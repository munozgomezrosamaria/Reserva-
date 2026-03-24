from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Reservation
from apps.services.models import Service

@login_required
def reserva(request):
    if request.method == "POST":
        date = request.POST.get("date")
        number_persons = int(request.POST.get("number_persons"))
        service_id = request.POST.get("service")

        service = get_object_or_404(Service, id=service_id)

        Reservation.objects.create(
            date=date,
            number_persons=number_persons,
            state="pendiente",
            user=request.user,
            service=service
        )

        return redirect("reservations")

    services = Service.objects.all()
    reservations = Reservation.objects.all()

    return render(request, "reservations.html", {
        "services": services,
        "reservations": reservations
    })