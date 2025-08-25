"""Model serializers"""

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


User = get_user_model()


# Create your serializers here.
class UserSerializer(ModelSerializer):
    """User serializer"""

    class Meta:
        """Meta data"""

        model = User
        read_only_fields = ["is_active", "is_staff", "is_superuser"]
        fields = [
            "id",
            "url",
            "is_active",
            "is_staff",
            "is_superuser",
            "photo",
            "username",
            "first_name",
            "last_name",
            "email",
        ]
