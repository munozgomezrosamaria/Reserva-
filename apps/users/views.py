from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from apps.common.forms.base import BaseBootstrapModelForm

class RegisterView(CreateView, BaseBootstrapModelForm):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy ("login")
    
