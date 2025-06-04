"""Custom API access permissions"""

from rest_framework.permissions import BasePermission


# Create your permissions here.
class IsOwner(BasePermission):
    """Allows access only to owner of the object"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is the owner of the object"""

        return request.user.id == obj.user.id


class IsAccountOwner(BasePermission):
    """Allows access only to owner of the user object"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is the owner of the user object"""

        return request.user == obj


class DenyAll(BasePermission):
    """Deny all requests"""

    def has_permission(self, request, view) -> bool:
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        return False
