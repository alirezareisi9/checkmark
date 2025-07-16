from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import UserInfo

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin) :
    fieldsets = [
        (
            'User Information',
            {
                'fields': ['username', 'password', 'first_name', 'last_name', 'phone_number', 'national_code', 
            'employee_code', 'is_active', 'is_staff', 'is_superuser', 'role', 'manager', 'leave_limit'],
            },
        ),
    ]
    list_display = ('username', 'first_name', 'last_name', 'role')
    list_filter = ('role',)

