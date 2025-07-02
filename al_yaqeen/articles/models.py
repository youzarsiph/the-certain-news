"""
Article model

Fields:
- user: Article owner
- category: Article category
- image: Article image
- title: Article title
- headline: Article headline
- content: Article content
- is_breaking: Designates if the Article is in breaking news
- updated_at: Last update
- created_at: Date published
- recommendations: Similar articles
- tags: Article tags

Methods:
- comment_count: Number of comments of an article
- reaction_count: Number of reactions of an article
- star_count: Number of stargazers of an article
- recommendation_count: Number of recommendations of an article
- tag_count: Number of tags of an article
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from al_yaqeen.mixins.models import DateTimeMixin
from al_yaqeen.ui.cms.blocks import CommonContentBlock


# Create your models here.
class Article(DateTimeMixin, Page):
    """News Articles"""

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
        related_name="+",
        help_text=_("Article image"),
    )
    headline = models.CharField(
        max_length=256,
        db_index=True,
        help_text=_("Article headline"),
    )
    content = StreamField(
        CommonContentBlock(),
        help_text=_("Article content"),
    )
    is_breaking = models.BooleanField(
        default=False,
        help_text=_("Designates if the Article is in breaking news"),
    )
    tags = ClusterTaggableManager(
        blank=True,
        through="tags.Tag",
    )
    recommendations = models.ManyToManyField(
        "self",
        symmetrical=True,
        help_text=_("Similar articles"),
    )

    # Dashboard UI config
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

    # Search
    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("headline"),
        index.SearchField("content"),
        index.FilterField("is_breaking"),
        index.FilterField("updated_at"),
        index.FilterField("created_at"),
    ]

    # API fields
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

    def __str__(self) -> str:
        return self.title
