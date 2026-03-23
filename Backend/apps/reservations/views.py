from django.shortcuts import render, redirect
from .models import Reservation
from .models import Service

def reserva(request):
    if request.method == "POST":
        date = request.POST.get("date")
        number_persons = request.POST.get("number_persons")

        Reservation.objects.create(
            date=date,
            number_persons=number_persons,
            state="pendiente",
            user=request.user,
            service=Service.objects.first()  # ejemplo
        )

        return redirect("reservations")

    return render(request, "reservations.html")