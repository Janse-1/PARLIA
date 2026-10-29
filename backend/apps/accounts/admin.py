from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'program', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('program', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Académica Uniguajira', {'fields': ('program',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Académica Uniguajira', {'fields': ('email', 'first_name', 'last_name', 'program')}),
    )
