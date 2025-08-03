from . import models


def get_role_label(choice_value):
    for value, label in models.RoleChoices.ROLE_CHOICES:
        if value == choice_value:
            return label