"""Serializers for al_yaqeen.articles"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.articles.models import Article


# Create your serializers here.
class ArticleSerializer(ModelSerializer):
    """Article Serializer"""

    class Meta:
        """Meta data"""

        model = Article
        read_only_fields = ["user", "recommendations"]
        fields = [
            "id",
            "url",
            "user",
            "category",
            "photo",
            "title",
            "headline",
            "content",
            "is_pinned",
            "stars",
            "tags",
            "recommendations",
            "comment_count",
            "reaction_count",
            "tag_count",
            "created_at",
            "updated_at",
        ]
