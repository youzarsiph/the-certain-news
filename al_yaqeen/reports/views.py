"""API endpoints for al_yaqeen.reports"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from al_yaqeen.reports.models import Report
from al_yaqeen.reports.serializers import ReportSerializer
from al_yaqeen.mixins import OwnerMixin


# Create your views here.
class ReportViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete Reports"""

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    search_fields = ["message"]
    filterset_fields = ["user", "article", "reason"]
    ordering_fields = ["created_at", "updated_at"]

    def get_permissions(self):
        """Allow users to create reports"""

        if self.action == "create":
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
