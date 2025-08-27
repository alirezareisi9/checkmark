# third-party
from django.contrib.auth.base_user import BaseUserManager
# local
from . import models, helpers, choices


class CustomUserManager(BaseUserManager) :

    use_in_migrations = True

    def _create_user(self, password, **extra_fields) :
        # breakpoint()
        # Check each required and username fields not be null
        required = iter(self.model.REQUIRED_FIELDS)  # gen
        for field in required:
            if not extra_fields.get(field):
                raise ValueError(f'{field} must be set!!')

        username_field = self.model.USERNAME_FIELD
        if not extra_fields.get(username_field):
            raise ValueError(f'{username_field} must be set!!')


        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # self._db for choose default device

        return user


    def create_user(self, password, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(password=password, **extra_fields)


    def create_superuser(self, password, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        # Check Role
        role = extra_fields.get('role')
        if role not in (choices.RoleChoices.MANAGER_CHOICE, choices.RoleChoices.ADMIN_CHOICE):
            raise ValueError(f'role must be {helpers.get_role_label(choices.RoleChoices.MANAGER_CHOICE)} or {helpers.get_role_label(choices.RoleChoices.ADMIN_CHOICE)}')

        return self._create_user(password=password, **extra_fields)
