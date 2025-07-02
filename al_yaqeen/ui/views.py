"""Views for al_yaqeen.ui"""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from al_yaqeen.articles.models import Article
from al_yaqeen.comments.models import Comment
from al_yaqeen.ui import mixins
from al_yaqeen.ui.forms import UserCreateForm


# Create your views here.
class AboutView(generic.TemplateView):
    """About page"""

    template_name = "ui/about.html"


class ContactView(generic.TemplateView):
    """Contact page"""

    template_name = "ui/contact.html"


# Auth views
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
    fields = ["first_name", "last_name", "email"]
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


class ArticleListView(BaseArticleListView, FilterView, generic.ListView):
    """Article list"""

    filterset_fields = ["is_breaking"]
    template_name = "ui/articles/list.html"


class ArticleYearView(BaseArticleListView, generic.YearArchiveView):
    """Year archive for articles"""

    allow_empty = True
    allow_future = True
    make_object_list = True
    template_name = "ui/articles/archive/year.html"


class ArticleMonthView(BaseArticleListView, generic.MonthArchiveView):
    """Month archive for articles"""

    month_format = "%m"
    template_name = "ui/articles/archive/month.html"


class ArticleDayView(BaseArticleListView, generic.DayArchiveView):
    """Week archive for articles"""

    month_format = "%m"
    template_name = "ui/articles/archive/day.html"


class ArticleDetailView(generic.DateDetailView):
    """Article details"""

    month_format = "%m"
    date_field = "created_at"
    template_name = "ui/articles/id.html"
    queryset = Article.objects.live().public()


# Comments
class CommentCreateView(LoginRequiredMixin, mixins.OwnerMixin, generic.CreateView):
    """Create a new comment"""

    model = Comment
    fields = ["content"]
    template_name = "ui/comments/new.html"


class CommentUpdateView(LoginRequiredMixin, mixins.OwnerMixin, generic.UpdateView):
    """Update a comment"""

    model = Comment
    fields = ["content"]
    template_name = "ui/comments/new.html"


class CommentDeleteView(LoginRequiredMixin, mixins.OwnerMixin, generic.DeleteView):
    """Delete a comment"""

    model = Comment
    template_name = "ui/comments/new.html"
