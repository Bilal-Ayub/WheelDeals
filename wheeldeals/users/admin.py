from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model"""

    model = CustomUser
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_guest",
        "phone",
        "city",
        "is_staff",
    ]
    list_filter = UserAdmin.list_filter + ("role", "is_guest")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("phone", "city", "role", "is_guest")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("phone", "city", "role", "is_guest")}),
    )
