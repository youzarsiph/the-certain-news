"""Serializers for al_yaqeen.tags"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.tags.models import Tag


# Create your serializers here.
class TagSerializer(ModelSerializer):
    """Tag Serializer"""

    class Meta:
        """Meta data"""

        model = Tag
        fields = [
            "id",
            "url",
            "name",
            "color",
            "description",
            "article_count",
            "created_at",
            "updated_at",
        ]
