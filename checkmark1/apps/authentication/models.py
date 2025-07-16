from .managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random



class CustomUserManager(BaseUserManager) :

    def create_user(self, username, **extra_fields) :
        user = self.model(username=username, **extra_fields)
        user.save(using=self._db)  # self._db for choice default device
        return user
    
    def create_superuser(self, username, **extra_fields) :
        user = self.model(username=username, **extra_fields)

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        # if you wanna restrict on creating superuser make below code usable
        # if extra_fields.get("role") is not RoleChoices.MANAGER_CHOICE :
        #     raise ValueError("Superuser must be manager")

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )
        return self.create_user(username=username, **extra_fields)


class RoleChoices() :  #define variables for role field choices
    EMPLOYEE_CHOICE = 'EMPLOYEE'
    REPORTER_CHOICE = 'REPORTER'
    MANAGER_CHOICE = 'MANAGER'
    ADMIN_CHOICE = 'ADMIN'
    #role field choices

    ROLE_CHOICES = [
        (EMPLOYEE_CHOICE, 'Employee'),
        (REPORTER_CHOICE, 'Reporter'),
        (MANAGER_CHOICE, 'Manager'),
        (ADMIN_CHOICE, 'ADMIN'),   
    ]


class UserInfo(AbstractUser) :
    #fields in AbstractUser : username, password, first_name, last_name, last_login, email, is_staff, is_active, date_joined
    first_name = models.CharField(max_length=255)  # allow_unicode nokay
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    national_code = models.CharField(max_length=10)
    employee_code = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=RoleChoices.ROLE_CHOICES, default=RoleChoices.EMPLOYEE_CHOICE)
    manager = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    change_password = models.DateField(auto_now_add=True)
    leave_limit = models.SmallIntegerField(null=True) # It should'nt be null but for make superuser I make it null
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # make email none
    email = None
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['national_code', 'employee_code', 'role']

    # link model to manager model
    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        default_password = '12345678'
        #PasswordInfo.first_password = default_password
        self.set_password(default_password)
        super().save(*args, **kwargs)  # Call the "real" save() method.

    # to how show instance
    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name