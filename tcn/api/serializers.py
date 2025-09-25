"""Model serializers"""

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from tcn.apps.articles.models import Article

User = get_user_model()


# Create your serializers here.
class UserSerializer(ModelSerializer):
    """User serializer"""

    class Meta:
        """Meta data"""

        model = User
        fields = [
            "id",
            "url",
            "photo",
            "username",
            "slug",
            "first_name",
            "last_name",
            "email",
        ]


class ArticleSerializer(ModelSerializer):
    """Article serializer"""

    class Meta:
        """Meta data"""

        model = Article
        fields = ["id", "title", "slug"]
        read_only_fields = ["id", "title", "slug"]
