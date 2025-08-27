# lib
# third-party
from rest_framework import permissions
# local
from . import choices


class IsManagerOrReadOnly(permissions.BasePermission):
    
    # Called for every request (list, create, detail, etc).
    # Typically used for general checks not tied to a specific object.
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.role in [choices.RoleChoices.MANAGER_CHOICE, choices.RoleChoices.ADMIN_CHOICE]
        return False
    
    
    # Called only on requests where an object is involved: retrieve, update, destroy.
    # Typically used for per-object checks.
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in [choices.RoleChoices.MANAGER_CHOICE, choices.RoleChoices.ADMIN_CHOICE]