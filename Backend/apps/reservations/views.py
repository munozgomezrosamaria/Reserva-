from django.shortcuts import render, redirect
from .models import Reservation
from .models import Service

def reserva(request):
    if request.method == "POST":
        date = request.POST.get("date")
        number_persons = request.POST.get("number_persons")
        service_id = request.POST.get("service")

        service = Service.objects.get(id=service_id)

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