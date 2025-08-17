"""Serializers for tcn.apps.comments"""

from rest_framework.serializers import ModelSerializer

from tcn.apps.comments.models import Comment


# Create your serializers here.
class CommentSerializer(ModelSerializer):
    """Comment Serializer"""

    class Meta:
        """Meta data"""

        model = Comment
        read_only_fields = ["owner", "article", "replies"]
        fields = [
            "id",
            "url",
            "owner",
            "article",
            "content",
            "replies",
            "created_at",
            "updated_at",
        ]
