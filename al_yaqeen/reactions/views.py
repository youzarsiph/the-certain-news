"""API endpoints for al_yaqeen.reactions"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_yaqeen.mixins import OwnerMixin
from al_yaqeen.reactions.models import Reaction
from al_yaqeen.reactions.serializers import ReactionSerializer


# Create your views here.
class ReactionViewSet(OwnerMixin, ModelViewSet):
    """Create, read, update and delete reactions"""

    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["emoji"]
    filterset_fields = ["user", "article", "emoji"]
    ordering_fields = ["created_at", "updated_at"]
