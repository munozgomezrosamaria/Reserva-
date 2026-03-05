from django.urls import path
from .views import RegisterView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "recover_password/",
        auth_views.PasswordResetView.as_view(
            template_name="users/recover_password.html"
        ),
        name="recover_password"
    ),
]