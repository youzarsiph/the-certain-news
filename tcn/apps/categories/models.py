"""Data Models for tcn.apps.categories"""

from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from tcn.apps.mixins import DateTimeMixin


# Create your models here.
class CategoryIndex(DateTimeMixin, Page):
    """Category index page"""

    description = RichTextField(help_text=_("Page description"))

    context_object_name = "index"
    template = "ui/categories/index.html"
    content_panels = Page.content_panels + [FieldPanel("description")]
    page_description = _("Category index page")

    parent_page_types = ["home.Home"]
    subpage_types = ["categories.Category"]

    class Meta(Page.Meta):
        """Meta data"""

        verbose_name = _("Category index page")


class Category(DateTimeMixin, Page):
    """Categories"""

    description = RichTextField(help_text=_("Category description"))
    display_owner = models.BooleanField(
        default=False,
        help_text=_("Wether to display the name of the owner of news article"),
    )

    show_in_menus = True
    context_object_name = "category"
    template = "ui/categories/id.html"
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

    api_fields = [APIField("description")]

    parent_page_types = ["categories.CategoryIndex"]
    subpage_types = ["articles.Article"]

    def get_context(self, request, *args, **kwargs):
        """Sort news articles"""

        context = super().get_context(request, *args, **kwargs)

        queryset = self.get_children().specific().order_by("-article__created_at")
        page_size = self.get_paginate_by(queryset)

        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size, request, kwargs
            )
            context = {
                **context,
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "object_list": queryset,
            }
        else:
            context = {
                **context,
                "paginator": None,
                "page_obj": None,
                "is_paginated": False,
                "object_list": queryset,
            }

        context["articles"] = queryset
        context.update(kwargs)

        return context

    class Meta:
        """Meta data"""

        verbose_name_plural = "categories"

    allow_empty = True
    paginate_by = 25
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = "page"

    def paginate_queryset(
        self,
        queryset,
        page_size,
        request,
        kwargs,
    ):
        """Paginate the queryset, if needed."""

        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_kwarg = self.page_kwarg
        page = kwargs.get(page_kwarg) or request.GET.get(page_kwarg) or 1

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
            return (paginator, page, page.object_list, page.has_other_pages())

        except InvalidPage as e:
            raise Http404(
                _("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """

        return self.paginate_by

    def get_paginator(
        self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs
    ):
        """Return an instance of the paginator for this view."""

        return self.paginator_class(
            queryset,
            per_page,
            orphans=orphans,
            allow_empty_first_page=allow_empty_first_page,
            **kwargs,
        )

    def get_paginate_orphans(self):
        """
        Return the maximum number of orphans extend the last page by when
        paginating.
        """

        return self.paginate_orphans

    def get_allow_empty(self):
        """
        Return ``True`` if the view should display empty lists and ``False``
        if a 404 should be raised instead.
        """

        return self.allow_empty
