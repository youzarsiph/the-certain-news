"""Data Models for al_yaqeen.categories"""

from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
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
    template = "ui/categories/id.html"
    content_panels = Page.content_panels + [FieldPanel("description")]
    page_description = _(
        "Categories help organize articles into thematic or subject-related groupings, "
        "making it easier for users to explore and filter available articles."
    )

    # Search fields
    search_fields = Page.search_fields + [index.SearchField("description")]

    # API fields
    api_fields = [APIField("description")]

    parent_page_types = ["home.Home"]
    subpage_types = ["articles.Article"]

    class Meta:
        """Meta data"""

        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.title

    def get_context(self, request):
        """Update context to order and paginate the articles"""

        page_size = 25
        queryset = (
            self.get_children()
            .live()
            .public()
            .specific()
            .order_by("-article__created_at")
        )
        paginator = Paginator(queryset, page_size, 10, True)

        page = request.GET.get("page") or 1

        try:
            page_number = int(page)

        except ValueError:
            if page == "last":
                page_number = paginator.num_pages

            else:
                raise Http404(
                    _("Page is not “last”, nor can it be converted to an int.")
                )
        try:
            page = paginator.page(page_number)

            is_paginated = page.has_other_pages()

            return {
                **super().get_context(request),
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "articles": queryset,
            }

        except InvalidPage as e:
            raise Http404(
                _("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )
