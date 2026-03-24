from django.urls import path
from .views import RegisterView
from django.contrib.auth import views as auth_views
from .views import RegisterView, UserLoginView
app_name = 'users'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "recover_password/",
        auth_views.PasswordResetView.as_view(
            template_name="users/recover_password.html"
        ),
        name="recover_password"
    ),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
]