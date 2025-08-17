"""Serializers for tcn.apps.reactions"""

from rest_framework.serializers import ModelSerializer

from tcn.apps.reactions.models import Reaction


# Create your serializers here.
class ReactionSerializer(ModelSerializer):
    """Reaction Serializer"""

    class Meta:
        """Meta data"""

        model = Reaction
        read_only_fields = ["owner", "article"]
        fields = [
            "id",
            "url",
            "owner",
            "article",
            "emoji",
            "created_at",
            "updated_at",
        ]
