from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado")

        return email