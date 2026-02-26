from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.views.generic import TemplateView
from apps.common.forms.base import BaseBootstrapModelForm

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html" 


class RegisterView(CreateView, BaseBootstrapModelForm):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy ("login")
    
