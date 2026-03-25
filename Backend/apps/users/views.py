from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm
from apps.common.forms.base import BaseBootstrapModelForm

from django.contrib.auth.views import LoginView
from django.contrib import messages

from django.core.mail import send_mail
from django.http import HttpResponse

def prueba_email(request):
    send_mail(
        "Prueba",
        "Este es un correo de prueba",
        "reservas.topaz@gmail.com",
        ["reservas.topaz@gmail.com"],
        fail_silently=False,
    )
    return HttpResponse("Correo enviado")

class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Correo o contraseña incorrectos")
        return super().form_invalid(form)

class RegisterView(CreateView, BaseBootstrapModelForm):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            "✅ Tu cuenta se registró correctamente. Ahora puedes iniciar sesión."
        )

        return response
    