"""Custom API access permissions"""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet


# Create your permissions here.
class DenyAll(BasePermission):
    """Deny all requests"""

    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return False

    def has_object_permission(self, request: Request, view: ModelViewSet, obj) -> bool:
        return False


class IsAccountOwner(BasePermission):
    """Check if the user is the owner of the account"""

    def has_object_permission(self, request: Request, view: ModelViewSet, obj) -> bool:
        return request.user == obj


class IsOwner(BasePermission):
    """Check if the user is the owner of the obj"""

    def has_object_permission(self, request: Request, view: ModelViewSet, obj) -> bool:
        return request.user.id == obj.owner_id
