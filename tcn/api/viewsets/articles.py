"""API endpoints for tcn.apps.articles"""

from rest_framework.permissions import IsAuthenticated
from wagtail.api.v2.views import PagesAPIViewSet

from tcn.apps.articles.models import Article


# Create your views here.
class ArticleViewSet(PagesAPIViewSet):
    """News Article APIs"""

    model = Article
    name = "articles"
    permission_classes = [IsAuthenticated]
    ordering_fields = ["created_at", "updated_at"]
