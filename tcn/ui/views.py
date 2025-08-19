"""Views for tcn.ui"""

from typing import Any

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.utils.translation import get_language_from_request
from django_filters.views import FilterView
from wagtail.contrib.search_promotions.models import Query

from tcn.apps.articles.models import Article
from tcn.apps.links.models import Link
from tcn.ui import mixins
from tcn.ui.forms import UserCreateForm

# Create your views here.
User = get_user_model()


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """Profile page"""

    template_name = "registration/profile.html"


class SignupView(SuccessMessageMixin, generic.CreateView):
    """Create a new user"""

    model = User
    form_class = UserCreateForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("ui:profile")
    success_message = _("Your account was created successfully!")


class UserDetailView(generic.DetailView):
    """User detail view"""

    model = User
    template_name = "ui/authors/id.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add articles to context"""

        context = super().get_context_data(**kwargs)

        return {
            **context,
            "articles": Article.objects.live()
            .public()
            .filter(owner=context["user"])
            .order_by("-created_at"),
        }


class UserUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AccountOwnerMixin,
    generic.UpdateView,
):
    """Update a user"""

    model = User
    success_url = reverse_lazy("ui:profile")
    template_name = "registration/edit.html"
    success_message = _("Your account was updated successfully!")
    fields = [
        "photo",
        "username",
        "first_name",
        "last_name",
        "email",
        "bio",
        "country",
        "phone",
    ]


class UserDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AccountOwnerMixin,
    generic.DeleteView,
):
    """Delete a user"""

    model = User
    success_url = reverse_lazy("ui:profile")
    template_name = "registration/delete.html"
    success_message = _("Your account was deleted successfully!")


class LinkRedirectView(generic.DetailView):
    """Redirect to news article"""

    model = Link

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> mixins.HttpResponse:
        """Redirect to news article"""

        link = self.get_object()

        if request.user.is_authenticated and not link.views.contains(self.request.user):
            link.views.add(self.request.user)

        return redirect(link.article.get_url())


# Articles
class BaseArticleListView:
    """Base class for article list views"""

    model = Article
    paginate_by = 25
    allow_empty = True
    allow_future = True
    ordering = "-created_at"
    date_field = "created_at"
    context_object_name = "articles"
    queryset = Article.objects.live().public()
    filterset_fields = ["is_breaking"]

    def get_queryset(self) -> mixins.QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(
                locale__language_code=get_language_from_request(
                    self.request, check_path=True
                )
            )
        )


class ArticleListView(BaseArticleListView, FilterView, generic.ListView):
    """Article list"""

    template_name = "ui/articles/list.html"


class SearchView(ArticleListView):
    """Search View"""

    template_name = "ui/search.html"
    context_object_name = "search_results"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Search new article"""

        return {
            **super().get_context_data(**kwargs),
            "search_query": self.request.GET.get("search", None),
            "search_results": self.get_search_results(),
        }

    def get_search_results(self):
        """Search news articles and return results"""

        queryset = self.get_queryset()
        search_query = self.request.GET.get("search", None)

        search_results = queryset.none()

        if search_query:
            search_results = queryset.search(search_query)

            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()

        return search_results


class ArticleArchiveView(BaseArticleListView, generic.ArchiveIndexView):
    """Article archive index"""

    template_name = "ui/articles/archive/index.html"


class ArticleYearView(BaseArticleListView, generic.YearArchiveView):
    """Year archive for articles"""

    template_name = "ui/articles/archive/year.html"


class ArticleMonthView(BaseArticleListView, generic.MonthArchiveView):
    """Month archive for articles"""

    month_format = "%m"
    template_name = "ui/articles/archive/month.html"


class ArticleDayView(BaseArticleListView, generic.DayArchiveView):
    """Day archive for articles"""

    month_format = "%m"
    template_name = "ui/articles/archive/day.html"


class ArticleDetailView(generic.DateDetailView):
    """Article details"""

    month_format = "%m"
    date_field = "created_at"
    template_name = "ui/articles/id.html"
    queryset = Article.objects.live().public()
