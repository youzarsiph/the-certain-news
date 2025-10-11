"""Data Models for tcn.apps.categories"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from tcn.apps.mixins import ChildPaginatorMixin, DateTimeMixin


# Create your models here.
class CategoryIndex(DateTimeMixin, Page):
    """Category index page"""

    description = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("description"),
        help_text=_("Page description"),
    )

    context_object_name = "index"
    template = "tcn/categories/index.html"
    content_panels = Page.content_panels + [FieldPanel("description")]
    page_description = _("Category index page")

    api_fields = [APIField("description", serializer=RichTextField())]

    parent_page_types = ["home.Home"]
    subpage_types = ["categories.Category"]

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Category index page")
        verbose_name_plural = _("Category index pages")


class Category(DateTimeMixin, ChildPaginatorMixin, Page):
    """Categories"""

    description = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("description"),
        help_text=_("Category description"),
    )
    display_owner = models.BooleanField(
        default=False,
        verbose_name=_("show owner"),
        help_text=_("Wether to display the name of the owner of news article"),
    )

    show_in_menus = True
    context_object_name = "category"
    template = "tcn/categories/id.html"
    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("display_owner"),
    ]
    page_description = _(
        "Categories help organize news article into thematic or subject-related groupings, "
        "making it easier for users to explore and filter available news article."
    )

    search_fields = Page.search_fields + [
        index.SearchField("description"),
        index.FilterField("display_owner"),
    ]

    api_fields = [
        APIField("display_owner"),
        APIField("description", serializer=RichTextField()),
    ]

    parent_page_types = ["categories.CategoryIndex"]
    subpage_types = ["articles.Article"]

    class Meta:
        """Meta data"""

        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def get_ordered_children(self):
        """Order the children of category"""

        return self.get_children().order_by("-article__created_at")
