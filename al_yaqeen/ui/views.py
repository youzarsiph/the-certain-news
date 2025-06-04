"""Views for al_yaqeen.ui"""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from al_yaqeen.articles.models import Article
from al_yaqeen.categories.models import Category
from al_yaqeen.comments.models import Comment
from al_yaqeen.ui import mixins
from al_yaqeen.ui.forms import UserCreateForm


# Create your views here.
class HomeView(generic.TemplateView):
    """Home page"""

    template_name = "ui/index.html"


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


# Categories
class CategoryListView(generic.ListView):
    """Category list"""

    paginate_by = 25
    ordering = "-created_at"
    template_name = "ui/categories/list.html"
    queryset = Category.objects.all()


class CategoryDetailView(generic.DetailView):
    """Category list"""

    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "ui/categories/id.html"
    queryset = Category.objects.prefetch_related("articles")


# Articles
class ArticleListView(generic.ListView):
    """Article list"""

    paginate_by = 25
    ordering = "-created_at"
    template_name = "ui/articles/list.html"
    queryset = Article.objects.live().public()


class ArticleDetailView(generic.DetailView):
    """Article list"""

    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "ui/articles/id.html"
    queryset = Article.objects.live().public()


# Comments
class BaseCommentView(mixins.OwnerMixin):
    """Base view for overriding methods"""

    def get_success_url(self) -> str:
        return reverse_lazy("ui:article", [self.object.id])


class CommentCreateView(LoginRequiredMixin, BaseCommentView, generic.CreateView):
    """Create a new comment"""

    model = Comment
    fields = ["content"]
    template_name = "ui/comments/new.html"


class CommentUpdateView(LoginRequiredMixin, BaseCommentView, generic.UpdateView):
    """Update a comment"""

    model = Comment
    fields = ["content"]
    template_name = "ui/comments/new.html"


class CommentDeleteView(LoginRequiredMixin, BaseCommentView, generic.DeleteView):
    """Delete a comment"""

    model = Comment
    fields = ["content"]
    template_name = "ui/comments/new.html"
