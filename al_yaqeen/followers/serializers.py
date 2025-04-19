"""Serializers for al_yaqeen.followers"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.followers.models import Follower


# Create your serializers here.
class FollowerSerializer(ModelSerializer):
    """Follower Serializer"""

    class Meta:
        """Meta data"""

        model = Follower
        read_only_fields = ["from_user", "to_user"]
        fields = [
            "id",
            "url",
            "from_user",
            "to_user",
            "created_at",
            "updated_at",
        ]
