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
    """Paginate the children of a page (Wagtail Page Model)"""

    allow_empty = True
    paginate_by = 25
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = "page"

    def get_ordered_children(self):
        return super().get_children()

    def get_context(self, request, *args, **kwargs):
        """Sort news articles"""

        context = super().get_context(request, *args, **kwargs)

        queryset = self.get_ordered_children()
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

        context["children"] = queryset
        context.update(kwargs)

        return context

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
