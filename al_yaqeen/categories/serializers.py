"""Serializers for al_yaqeen.categories"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.categories.models import Category


# Create your serializers here.
class CategorySerializer(ModelSerializer):
    """Category serializer"""

    class Meta:
        """Meta data"""

        model = Category
        fields = [
            "id",
            "url",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
