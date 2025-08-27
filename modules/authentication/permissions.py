# lib
# third-party
from rest_framework import permissions
# local
from . import choices


class IsManagerOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in [choices.RoleChoices.MANAGER_CHOICE, choices.RoleChoices.ADMIN_CHOICE]