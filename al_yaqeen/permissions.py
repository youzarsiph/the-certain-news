"""Custom permissions"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


# Create your permissions here.
class IsOwner(BasePermission):
    """Allows access only to owner of the object"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is the owner of the object"""

        return request.user == obj.user


class IsAccountOwner(BasePermission):
    """Allows access only to owner of the user object"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is the owner of the user object"""

        return request.user == obj


class IsReadOnly(BasePermission):
    """Allows read only access"""

    def has_permission(self, request, view):
        """Check request.method"""

        return request.method in SAFE_METHODS


class IsListOnly(BasePermission):
    """Allow access only to list action"""

    def has_permission(self, request, view):
        """Allow access to list action"""

        return view.action == "list"
