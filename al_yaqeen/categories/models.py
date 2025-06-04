"""Data Models for al_yaqeen.categories"""

from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from al_yaqeen.mixins.models import DateTimeMixin
from al_yaqeen.ui.cms.blocks import TextContentBlock


# Create your models here.
class Category(DateTimeMixin, Page):
    """Categories"""

    description = StreamField(
        TextContentBlock(),
        help_text=_("Category description"),
    )

    # Dashboard UI config
    show_in_menus = True
    context_object_name = "category"
    template = "ui/previews/category.html"
    content_panels = Page.content_panels + [FieldPanel("description")]
    page_description = _(
        "Categories help organize articles into thematic or subject-related groupings, "
        "making it easier for users to explore and filter available articles."
    )

    # Search fields
    search_fields = Page.search_fields + [index.SearchField("description")]

    # API fields
    api_fields = [APIField("description")]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["articles.Article"]

    class Meta:
        """Meta data"""

        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.title
