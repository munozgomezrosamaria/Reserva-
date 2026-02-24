from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.views.generic import TemplateView
# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html" 


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy ("login")
    
