"""View Mixins"""

from typing import Any, List, Mapping, Optional


# Create your mixins here.
class OwnerMixin:
    """Add the owner of the object"""

    def perform_create(self, serializer):
        """Save the object with owner"""

        serializer.save(user=self.request.user)


class UserFilterMixin:
    """Filter queryset by user"""

    def get_queryset(self):
        """Perform the filter"""

        return super().get_queryset().filter(user_id=self.request.user.id)


class ActionPermissionsMixin:
    """Allows you to set permissions for each action using a Mapping"""

    action_permissions: Optional[Mapping[str, List[Any]]] = None

    def get_permissions(self) -> List[Any]:
        """Set permissions based on each action"""

        if self.action_permissions:
            self.permission_classes = self.action_permissions.get(
                self.action, self.action_permissions["default"]
            )

        return super().get_permissions()


class ActionSerializersMixin:
    """Allows you to set Serializers for each action using a Mapping"""

    action_serializers: Optional[Mapping[str, Any]] = None

    def get_serializer_class(self):
        """Set serializer class based on action"""

        if self.action_serializers:
            self.serializer_class = self.action_serializers.get(
                self.action, self.action_serializers["default"]
            )

        return super().get_serializer_class()
