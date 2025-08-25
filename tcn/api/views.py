"""API views"""

from rest_framework.permissions import IsAuthenticated
from wagtail.api.v2.views import PagesAPIViewSet

from tcn.apps.articles.models import Article
from tcn.apps.categories.models import Category


# Create your views here.
class CategoryViewSet(PagesAPIViewSet):
    """News Categories APIs"""

    model = Category
    name = "categories"
    permission_classes = [IsAuthenticated]
    ordering_fields = ["created_at", "updated_at"]


class ArticleViewSet(PagesAPIViewSet):
    """News Articles APIs"""

    model = Article
    name = "articles"
    permission_classes = [IsAuthenticated]
    ordering_fields = ["created_at", "updated_at"]
