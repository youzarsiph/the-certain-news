"""Article model"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from tcn.apps.mixins import DateTimeMixin
from tcn.cms.blocks import MediaBlock


# Create your models here.
class Article(DateTimeMixin, Page):
    """News Articles"""

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("image"),
        help_text=_("Article image"),
    )
    headline = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name=_("headline"),
        help_text=_("Article headline"),
    )
    content = StreamField(
        MediaBlock(),
        verbose_name=_("content"),
        help_text=_("Article content"),
    )
    is_breaking = models.BooleanField(
        default=False,
        verbose_name=_("is breaking"),
        help_text=_("Designates if the Article is in breaking news"),
    )
    tags = ClusterTaggableManager(
        blank=True,
        through="tags.ArticleTag",
        verbose_name=_("tags"),
        help_text=_("Tags"),
    )
    recommendations = models.ManyToManyField(
        "self",
        symmetrical=True,
        help_text=_("recommendations"),
        verbose_name=_("Similar articles"),
    )

    context_object_name = "article"
    template = "ui/articles/id.html"
    page_description = _("News Articles")
    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("headline"),
        FieldPanel("content"),
        FieldPanel("is_breaking"),
        FieldPanel("tags"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("headline"),
        index.SearchField("content"),
        index.FilterField("is_breaking"),
        index.FilterField("updated_at"),
        index.FilterField("created_at"),
    ]

    api_fields = [
        APIField("image"),
        APIField("headline"),
        APIField("content"),
        APIField("is_breaking"),
        APIField("updated_at"),
        APIField("created_at"),
    ]

    parent_page_types = ["categories.Category"]
    subpage_types = []

    class Meta:
        """Meta data"""

        verbose_name = _("News article")
        verbose_name_plural = _("News articles")

    def get_context(self, request, *args, **kwargs):
        return {
            **super().get_context(request, *args, **kwargs),
            "recommendations": self.get_siblings(inclusive=False)
            .specific()
            .order_by("?")[:6],
        }

    def __str__(self) -> str:
        return self.title
