from django.contrib import admin
from .models import User, LoginHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "mobile")
    search_fields = ("full_name", "email", "mobile")
    exclude = ("password",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "status",
        "user",
        "ip_address",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("email", "ip_address")
    ordering = ("-created_at",)
    readonly_fields = (
        "email",
        "user",
        "status",
        "ip_address",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False