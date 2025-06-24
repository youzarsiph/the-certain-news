"""Serializers for al_yaqeen.articles"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.articles.models import Article


# Create your serializers here.
class ArticleSerializer(ModelSerializer):
    """Article Serializer"""

    class Meta:
        """Meta data"""

        model = Article
        read_only_fields = ["owner"]
        fields = [
            "id",
            "url",
            "owner",
            "is_breaking",
            "image",
            "title",
            "headline",
            "content",
            "created_at",
            "updated_at",
        ]
