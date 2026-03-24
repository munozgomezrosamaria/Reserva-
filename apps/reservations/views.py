from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Reservation
from apps.users.models import CustomUser

@staff_member_required
def admin_reservations(request):
    reservations = Reservation.objects.select_related('user', 'service').all()
    return render(request, 'reservations/admin_reservations.html', {
        'reservations': reservations
    })

@staff_member_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.state = request.POST.get('state')
        reservation.save()
        return redirect('reservations:admin_reservations')
    return render(request, 'reservations/edit_reservation.html', {
        'reservation': reservation
    })

@staff_member_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations:admin_reservations')
    return render(request, 'reservations/delete_reservation.html', {
        'reservation': reservation
    })

@staff_member_required
def admin_users(request):
    users = CustomUser.objects.all()
    return render(request, 'reservations/admin_users.html', {
        'users': users
    })