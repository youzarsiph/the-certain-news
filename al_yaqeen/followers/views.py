"""API endpoints for al_yaqeen.followers"""

from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_yaqeen.followers.models import Follower
from al_yaqeen.followers.serializers import FollowerSerializer
from al_yaqeen.permissions import IsListOnly, IsReadOnly


# Create your views here.
class FollowerViewSet(ModelViewSet):
    """Create, read, update and delete Followers"""

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated, IsReadOnly, IsListOnly]
    filterset_fields = ["from_user", "to_user"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        """Filter queryset by request.user"""

        return (
            super()
            .get_queryset()
            .filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))
        )
