# local
from . import choices


def get_role_label(choice_value):
    for value, label in choices.RoleChoices.ROLE_CHOICES:
        if value == choice_value:
            return label