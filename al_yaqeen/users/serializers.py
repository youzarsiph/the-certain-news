"""Serializers for al_yaqeen.users"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.users.models import User


# Create your serializers here.
class UserSerializer(ModelSerializer):
    """User Serializer"""

    class Meta:
        """Meta data"""

        model = User
        fields = [
            "id",
            "url",
            "photo",
            "username",
            "first_name",
            "last_name",
            "bio",
            "article_count",
            "follower_count",
        ]
