from django.contrib import admin

from users.models import CustomUser, VerificationCode


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "code", "last_sent_time", "expired_at", "is_verified"]
    ordering = ["-last_sent_time"]
