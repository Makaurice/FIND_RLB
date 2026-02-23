from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('role', 'bio', 'phone', 'address', 'city', 'state', 'zip_code', 'profile_image', 'is_verified')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active']
    list_filter = UserAdmin.list_filter + ('role', 'is_verified')

admin.site.register(User, CustomUserAdmin)
