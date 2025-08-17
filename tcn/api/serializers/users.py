"""Serializers for tcn.apps.users"""

from rest_framework.serializers import ModelSerializer

from tcn.apps.users.models import User


# Create your serializers here.
class UserSerializer(ModelSerializer):
    """User serializer"""

    class Meta:
        """Meta data"""

        model = User
        read_only_fields = ["is_active", "is_staff", "is_instructor"]
        fields = [
            "id",
            "url",
            "is_active",
            "is_staff",
            "is_instructor",
            "photo",
            "username",
            "first_name",
            "last_name",
            "email",
        ]
