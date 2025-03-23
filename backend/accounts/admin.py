
from accounts.models import (
    UserProfile,
)
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

User = get_user_model()


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ("email", "first_name", "last_name")
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_verified",
        "is_onboarded",
    )
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "ton_wallet_address",
                    "gender",
                    "date_of_birth", 
                    "location",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    'is_superuser',
                    "is_staff",
                    "is_verified",
                    "is_onboarded",
                    'groups',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    ordering = ("created_at",)

