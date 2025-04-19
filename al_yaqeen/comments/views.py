"""API endpoints for al_yaqeen.comments"""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_yaqeen.ai.views import CommentAIActions
from al_yaqeen.comments.models import Comment
from al_yaqeen.comments.serializers import CommentSerializer
from al_yaqeen.mixins import OwnerMixin


# Create your views here.
class CommentViewSet(OwnerMixin, CommentAIActions, ModelViewSet):
    """Create, read, update and delete Comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["content"]
    filterset_fields = ["user", "article"]
    ordering_fields = ["created_at", "updated_at"]

    @action(methods=["post"], detail=True)
    def reply(self, request: Request, pk: int) -> Response:
        """Reply to a comment"""

        # Get comment object
        obj = self.get_object()

        # Validate and save comment
        serializer = CommentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(user=request.user, article=obj.article)

        # Add comment to replies
        obj.replies.add(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
