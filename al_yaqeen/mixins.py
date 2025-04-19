"""Mixins"""

from rest_framework.permissions import IsAuthenticated
from al_yaqeen.permissions import IsOwner


# Create your mixins here.
class OwnerMixin:
    """Adds the owner automatically"""

    def get_permissions(self):
        """update permissions based on action"""

        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]

        return super().get_permissions()

    def perform_create(self, serializer):
        """Add user as self.request.user"""

        serializer.save(user=self.request.user)
