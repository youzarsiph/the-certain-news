"""Home page"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from tcn.apps.articles.models import Article
from tcn.apps.categories.models import Category
from tcn.cms.blocks import FooterStreamBlock, MediaBlock


class Home(Page):
    """Home page"""

    footer = StreamField(
        FooterStreamBlock(),
        min_num=1,
        max_num=1,
        verbose_name=_("footer"),
        help_text=_("Footer"),
    )

    template = "tcn/index.html"
    context_object_name = "home"
    parent_page_types = ["wagtailcore.Page"]
    content_panels = Page.content_panels + [FieldPanel("footer")]
    search_fields = Page.search_fields + [index.SearchField("footer")]

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")

    def get_context(self, request, *args, **kwargs):
        """Add extra context"""

        context = super().get_context(request, *args, **kwargs)
        articles = (
            Article.objects.descendant_of(self).live().public().prefetch_related("link")
        )

        return {
            **context,
            "trending_news": articles.order_by("link__view_count")[:10],
            "latest_news": articles.order_by("-created_at")[:9],
            "breaking_news": articles.filter(is_breaking=True).order_by("-created_at")[
                :9
            ],
            "categories": Category.objects.descendant_of(self)
            .live()
            .public()
            .order_by("?")[:5],
        }


class DetailPages(Page):
    """Pages to create details like terms, privacy policy, disclaimer"""

    content = StreamField(
        MediaBlock(),
        null=True,
        blank=True,
        verbose_name=_("content"),
        help_text=_("Page content"),
    )

    subpage_types = []
    template = "tcn/page.html"
    parent_page_types = ["home.Home"]
    content_panels = Page.content_panels + [FieldPanel("content")]
    search_fields = Page.search_fields + [index.SearchField("content")]
    page_description = _("Detail pages like terms, privacy policy, disclaimer")


class FormFields(AbstractFormField):
    page = ParentalKey(
        "home.FormDetailPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class FormDetailPage(AbstractEmailForm):
    """Page to create pages with forms like contact us, feedback"""

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

    subpage_types = []
    template = "tcn/form.html"
    parent_page_types = ["home.Home"]
    page_description = _("Page with form")

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
