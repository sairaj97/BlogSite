from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .models import Users


class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']


admin.site.register(Users, CustomUserAdmin)

