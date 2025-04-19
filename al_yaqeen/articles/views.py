"""API endpoints for al_yaqeen.articles"""

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_yaqeen.ai.views import ArticleAIActions
from al_yaqeen.articles.models import Article
from al_yaqeen.articles.serializers import ArticleRetrieveSerializer, ArticleSerializer
from al_yaqeen.followers.models import Follower
from al_yaqeen.mixins import OwnerMixin
from al_yaqeen.reactions.serializers import ReactionSerializer


# Create your views here.
class ArticleViewSet(OwnerMixin, ArticleAIActions, ModelViewSet):
    """Create, read, update and delete Articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "headline", "content"]
    filterset_fields = ["user", "category", "is_pinned", "tags"]
    ordering_fields = ["title", "created_at", "updated_at"]

    def get_serializer_class(self):
        """Return different serializer_class based on self.action"""

        match self.action:
            case "react":
                self.serializer_class = ReactionSerializer

            case "retrieve":
                self.serializer_class = ArticleRetrieveSerializer

            case "star":
                self.serializer_class = Serializer

            case _:
                pass

        return super().get_serializer_class()

    @action(methods=["post"], detail=True)
    def react(self, request: Request, pk: int) -> Response:
        """React to an article"""

        message: str

        # Get article object
        article = self.get_object()

        # Data validation
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(
                serializer.error_messages,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.request.user not in article.reactions.all():
            article.reactions.add(self.request.user)
            message = f"You reacted to {article} with {serializer.validated_data.get('emoji')}"

        else:
            article.reactions.remove(self.request.user)
            message = f"You un-reacted to {article}"

        return Response({"details": message}, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def star(self, request: Request, pk: int) -> Response:
        """Star an article"""

        message: str

        # Get article object
        article = self.get_object()

        # Data validation
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(
                serializer.error_messages,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.request.user not in article.stargazers.all():
            article.stargazers.add(self.request.user)
            message = f"Article {article} starred"

        else:
            article.stargazers.remove(self.request.user)
            message = f"Article {article} un-starred"

        return Response({"details": message}, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def popular(self, request: Request) -> Response:
        """Popular articles"""

        # Get queryset and filter
        queryset = self.filter_queryset(self.get_queryset()).order_by("-stargazers")

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Return the data
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def trending(self, request: Request) -> Response:
        """Trending articles"""

        # Get queryset and filter
        queryset = self.filter_queryset(self.get_queryset()).filter(
            created_at__gt=timezone.now()
        )

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Return the data
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def starred(self, request: Request) -> Response:
        """Starred articles"""

        # Get queryset and filter
        queryset = self.filter_queryset(self.get_queryset()).filter(
            stargazers=request.user
        )

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Return the data
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def feed(self, request: Request) -> Response:
        """Article feed"""

        # Get queryset and filter
        queryset = self.filter_queryset(self.get_queryset()).filter(
            user__in=[
                f.from_user for f in Follower.objects.filter(to_user=request.user)
            ]
        )

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Return the data
        return Response(serializer.data)
