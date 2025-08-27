# lib
import random
# third-party
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# local
from . import managers, choices





class CustomUser(AbstractUser) :
    #fields in AbstractUser : username, password, first_name, last_name, last_login, email, is_staff, is_active, is_superuser, date_joined
    first_name = models.CharField(max_length=255)  # allow_unicode nokay
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, unique=True)
    national_code = models.CharField(max_length=10, unique=True)  # check successfully : , validators=[MinLengthValidator(10)]
    employee_code = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=choices.RoleChoices.ROLE_CHOICES, default=choices.RoleChoices.EMPLOYEE_CHOICE)
    manager = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    change_password = models.BooleanField(default=False)
     # User should change his password first time login to account
    leave_limit = models.SmallIntegerField(null=True) 
     # It should'nt be null but for make superuser I make it null
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # make email and username none
    username = None
    email = None

    USERNAME_FIELD = 'employee_code'
    EMAIL_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['national_code', 'role', 'phone_number']

    # link model to manager model
    objects = managers.CustomUserManager()

    def __str__(self) -> str:
        return str(self.employee_code)
