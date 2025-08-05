from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from . import models
from . import forms

@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin) :
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    model = models.CustomUser
    list_display = ['last_name', 'employee_code', 'role', 'manager']
    list_filter = ['role', 'manager', 'date_joined']
    
    
    fieldsets = (
        (None, {'fields': ('employee_code', 'password',\
                           'first_name', 'last_name', 'phone_number', \
                            'national_code', 'role', 'manager',\
                              'change_password', 'leave_limit')}),
        ('Log', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )


    add_fieldsets = (
        (None, {'fields': ('employee_code', 'password1', 'password2', \
                           'first_name', 'last_name', 'phone_number', \
                            'national_code', 'role', 'manager',\
                              'change_password', 'leave_limit')}),
        ('Log', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )

    search_fields = ('last_name', 'employee_code')
    ordering = ('employee_code',)
    readonly_fields = ['last_login', 'date_joined', 'change_password']


    def get_form(self, request, obj, change, **kwargs):
        not_accessible_msg = 'It initializes automatically'
        help_texts =  {
            'change_password' : not_accessible_msg,
            'last_login' : not_accessible_msg,
            'date_joined' : not_accessible_msg,
        }
        kwargs.update({ 'help_texts':help_texts })
        return super().get_form(request=request, obj=obj, change=change, **kwargs)







#----------------------------------------------------------------------------------------------------------------
    # fieldsets = [
    #     (
    #         'User Information',
    #         {
    #             'fields': ['username', 'password', 'first_name', 'last_name', 'phone_number', 'national_code', 
    #         'employee_code', 'is_active', 'is_staff', 'is_superuser', 'role', 'manager', 'leave_limit'],
    #         },
    #     ),
    # ]
    # list_display = ('username', 'first_name', 'last_name', 'role')
    # list_filter = ('role',)

