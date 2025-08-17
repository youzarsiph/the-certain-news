"""Views for tcn.ui"""

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page

from tcn.apps.articles.models import Article
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
    success_message = "Your account was created successfully!"


class UserUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AccountOwnerMixin,
    generic.UpdateView,
):
    """Update a user"""

    model = User
    template_name = "registration/edit.html"
    fields = ["photo", "first_name", "last_name", "email", "bio", "country", "phone"]
    success_url = reverse_lazy("ui:profile")
    success_message = "Your account was updated successfully!"


class UserDeleteView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    mixins.AccountOwnerMixin,
    generic.DeleteView,
):
    """Delete a user"""

    model = User
    template_name = "registration/delete.html"
    success_url = reverse_lazy("ui:index")
    success_message = "Your account was deleted successfully!"


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
    filterset_fields = ["is_breaking", "locale__language_code"]


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


class ArticleYearView(BaseArticleListView, FilterView, generic.YearArchiveView):
    """Year archive for articles"""

    allow_empty = True
    allow_future = True
    make_object_list = True
    template_name = "ui/articles/archive/year.html"


class ArticleMonthView(BaseArticleListView, FilterView, generic.MonthArchiveView):
    """Month archive for articles"""

    month_format = "%m"
    template_name = "ui/articles/archive/month.html"


class ArticleDayView(BaseArticleListView, FilterView, generic.DayArchiveView):
    """Week archive for articles"""

    month_format = "%m"
    template_name = "ui/articles/archive/day.html"


class ArticleDetailView(generic.DateDetailView):
    """Article details"""

    month_format = "%m"
    date_field = "created_at"
    template_name = "ui/articles/id.html"
    queryset = Article.objects.live().public()
