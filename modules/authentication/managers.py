from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager) :

    # What happen when a user create
    def create_user(self, username, password=None, **extra_fields) :
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # self._db for choose default device
        return user

    # What happen when a superuser create
    def create_superuser(self, username, password, **extra_fields) :
        # for superuser should set this fields True
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        # If you wanna restrict on creating superuser make below code usable
        # if extra_fields.get("role") is not RoleChoices.MANAGER_CHOICE :
        #     raise ValueError("Superuser must be manager")

        return self.create_user(username=username, password=password, **extra_fields)