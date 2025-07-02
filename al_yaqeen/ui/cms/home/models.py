"""Home page"""

from wagtail.models import Page

from al_yaqeen.articles.models import Article
from al_yaqeen.categories.models import Category


class Home(Page):
    """Home page"""

    # Dashboard UI
    template = "ui/index.html"
    content_panels = Page.content_panels + []
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["categories.Category"]

    def get_context(self, request):
        """Update context to include only published news, ordered by reverse-chron"""

        return {
            **super().get_context(request),
            "breaking_news": Article.objects.live()
            .public()
            .filter(is_breaking=True)
            .order_by("-created_at")[:6],
            "latest_news": Article.objects.live().public().order_by("-created_at")[:6],
            "categories": Category.objects.live().public().order_by("-created_at")[:3],
        }
