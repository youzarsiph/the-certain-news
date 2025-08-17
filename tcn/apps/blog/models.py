"""Data Models for tcn.apps.blog"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from tcn.apps.mixins import DateTimeMixin
from tcn.cms.blocks import MediaBlock


# Create your models here.
class BlogIndex(DateTimeMixin, Page):
    """Blog index page"""

    context_object_name = "index"
    template = "ui/blog/index.html"
    page_description = _("Blog index page")

    parent_page_types = ["home.Home"]
    subpage_types = ["blog.Post"]

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Blog index page")

    def get_context(self, request, *args, **kwargs):
        """Sort blog posts and add to context"""

        context = super().get_context(request, *args, **kwargs)

        return {**context}


class Post(DateTimeMixin, Page):
    """Blog posts"""

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
        help_text=_("Post image"),
    )
    headline = models.CharField(
        max_length=128,
        db_index=True,
        help_text=_("Post headline"),
    )
    content = StreamField(
        MediaBlock(),
        help_text=_("Post content"),
    )
    tags = ClusterTaggableManager(
        blank=True,
        through="tags.PostTag",
        help_text=_("Post tags"),
    )

    context_object_name = "post"
    template = "ui/blog/post.html"
    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("headline"),
        FieldPanel("content"),
        FieldPanel("tags"),
    ]
    page_description = _("Blog Posts")

    search_fields = Page.search_fields + [
        index.SearchField("headline"),
        index.SearchField("content"),
    ]

    api_fields = [APIField("headline"), APIField("content"), APIField("tags")]

    parent_page_types = ["blog.BlogIndex"]
    subpage_types = []
