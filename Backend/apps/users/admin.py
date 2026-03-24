
"""@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = ("username","email","first_name","last_name","is_staff","is_superuser")"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("id","email", "first_name", "is_staff", "is_superuser")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("first_name",)}),
        ("Permisos", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)