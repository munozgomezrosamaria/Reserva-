from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('panel/reservations/', views.admin_reservations, name='admin_reservations'),
    path('panel/reservations/edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    path('panel/reservations/delete/<int:pk>/', views.delete_reservation, name='delete_reservation'),
    path('panel/users/', views.admin_users, name='admin_users'),
]