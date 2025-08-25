"""Home page"""

from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from tcn.apps.articles.models import Article
from tcn.apps.blog.models import BlogIndex
from tcn.apps.categories.models import Category, CategoryIndex
from tcn.cms.blocks import MediaBlock


class Home(Page):
    """Home page"""

    template = "ui/index.html"
    context_object_name = "home"
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "home.About",
        "home.Contact",
        "blog.BlogIndex",
        "categories.CategoryIndex",
        "categories.Category",
    ]

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")

    def get_context(self, request, *args, **kwargs):
        """Add extra context"""

        context = super().get_context(request, *args, **kwargs)

        return {
            **context,
            "about": self.get_children().type(About).last(),
            "contact": self.get_children().type(Contact).last(),
            "blog_index": self.get_children().type(BlogIndex).last(),
            "categories_index": self.get_children().type(CategoryIndex).last(),
            "random_news": Article.objects.descendant_of(self).live().order_by("?")[:3],
            "latest_news": Article.objects.descendant_of(self)
            .live()
            .order_by("-created_at")[:10],
            "breaking_news": Article.objects.descendant_of(self)
            .live()
            .filter(is_breaking=True)
            .order_by("-created_at")[:10],
            "categories": Category.objects.descendant_of(self).live().order_by("?")[:5],
        }


class About(Page):
    """About page"""

    content = StreamField(
        MediaBlock(),
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("Page content"),
    )

    template = "ui/about.html"
    context_object_name = "about"
    page_description = _("About us page")
    content_panels = Page.content_panels + [FieldPanel("content")]
    parent_page_types = ["home.Home"]
    subpage_types = []

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("About page")
        verbose_name_plural = _("About pages")


class Contact(Page):
    """Contact page"""

    content = StreamField(
        MediaBlock(),
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("Page content"),
    )

    template = "ui/contact.html"
    context_object_name = "contact"
    page_description = _("Contact us page")
    content_panels = Page.content_panels + [FieldPanel("content")]
    parent_page_types = ["home.Home"]
    subpage_types = []

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Contact page")
        verbose_name_plural = _("Contact pages")
