"""Serializers for al_yaqeen.categories"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.categories.models import Category


# Create your serializers here.
class CategorySerializer(ModelSerializer):
    """Category Serializer"""

    class Meta:
        """Meta data"""

        model = Category
        fields = [
            "id",
            "url",
            "name",
            "description",
            "article_count",
            "created_at",
            "updated_at",
        ]
