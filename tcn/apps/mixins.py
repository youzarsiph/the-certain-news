"""Model mixins"""

from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.http import Http404
from django.utils.translation import gettext_lazy as _


# Create your model mixins here.
class DateTimeMixin(models.Model):
    """Provide `created_at` and `updated_at` for a model"""

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last update"),
        help_text=_("Last update"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date created"),
        help_text=_("Date created"),
    )

    class Meta:
        """Meta data"""

        abstract = True


class ChildPaginatorMixin:
    """Paginate the children of a page"""

    def get_context(self, request):
        """Update context to order and paginate the articles"""

        page_size = 1
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
