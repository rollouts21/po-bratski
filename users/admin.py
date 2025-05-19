from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Персональная информация", {"fields": ("full_name", "email")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "email",
                    "full_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        "phone_number",
        "email",
        "full_name",
        "is_staff",
        "street",
        "house",
        "apartment",
        "entrance",
        "floor",
    )
    search_fields = ("phone_number", "email", "full_name")
    ordering = ("phone_number",)


admin.site.register(CustomUser, CustomUserAdmin)
