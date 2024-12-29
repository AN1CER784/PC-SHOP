from django.contrib import admin

from .models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
