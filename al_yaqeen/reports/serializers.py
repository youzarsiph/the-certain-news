"""Serializers for al_yaqeen.reports"""

from rest_framework.serializers import ModelSerializer

from al_yaqeen.reports.models import Report
from al_yaqeen.users.serializers import UserSerializer


# Create your serializers here.
class ReportSerializer(ModelSerializer):
    """Report Serializer"""

    user = UserSerializer(read_only=True)

    class Meta:
        """Meta data"""

        model = Report
        read_only_fields = ["user", "article"]
        fields = [
            "id",
            "url",
            "user",
            "article",
            "message",
            "reason",
            "created_at",
            "updated_at",
        ]
