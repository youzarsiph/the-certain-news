"""Home page"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from tcn.apps.articles.models import Article
from tcn.apps.categories.models import Category, CategoryIndex
from tcn.cms.blocks import MediaBlock


class Home(Page):
    """Home page"""

    template = "ui/index.html"
    context_object_name = "home"
    parent_page_types = ["wagtailcore.Page"]

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")

    def get_context(self, request, *args, **kwargs):
        """Add extra context"""

        context = super().get_context(request, *args, **kwargs)

        return {
            **context,
            "categories_index": self.get_children().type(CategoryIndex).last(),
            "trending_news": Article.objects.descendant_of(self)
            .live()
            .prefetch_related("link")
            .order_by("link__view_count")[:9],
            "latest_news": Article.objects.descendant_of(self)
            .live()
            .prefetch_related("link")
            .order_by("-created_at")[:9],
            "breaking_news": Article.objects.descendant_of(self)
            .live()
            .prefetch_related("link")
            .filter(is_breaking=True)
            .order_by("-created_at")[:9],
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


class FormField(AbstractFormField):
    page = ParentalKey(
        "home.Contact",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class Contact(AbstractEmailForm):
    """Contact page"""

    content = StreamField(
        MediaBlock(),
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("Page content"),
    )
    message = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("message"),
        help_text=_("Message to display after form submission"),
    )

    template = "ui/contact.html"
    context_object_name = "contact"
    page_description = _("Contact us page")
    parent_page_types = ["home.Home"]
    subpage_types = []

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("content"),
        FieldPanel("message"),
        FormSubmissionsPanel(),
        InlinePanel("form_fields"),
        MultiFieldPanel(
            [
                FieldPanel("subject"),
                FieldRowPanel([FieldPanel("from_address"), FieldPanel("to_address")]),
            ],
            "Email",
        ),
    ]
    search_fields = AbstractEmailForm.search_fields + [
        index.SearchField("content"),
        index.SearchField("message"),
    ]

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Contact page")
        verbose_name_plural = _("Contact pages")
