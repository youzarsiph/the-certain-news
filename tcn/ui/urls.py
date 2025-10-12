"""URLConf for tcn.ui"""

from django.contrib.auth import views as auth
from django.urls import include, path, reverse_lazy

from tcn.ui import views

# Create your URLConf here.
app_name = "tcn"


auth_urls = [
    path("accounts/login/", auth.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth.LogoutView.as_view(), name="logout"),
    path("accounts/subscribe/", views.SignupView.as_view(), name="subscribe"),
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "accounts/following/",
        views.UserListView.as_view(template_name="registration/users.html"),
        name="following",
    ),
    path(
        "accounts/<slug:slug>/edit/",
        views.UserUpdateView.as_view(),
        name="u-user",
    ),
    path(
        "accounts/<slug:slug>/delete/",
        views.UserDeleteView.as_view(),
        name="d-user",
    ),
    path(
        "accounts/password/change/",
        auth.PasswordChangeView.as_view(
            success_url=reverse_lazy("tcn:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "accounts/password/change/done/",
        auth.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "accounts/password/reset/",
        auth.PasswordResetView.as_view(
            success_url=reverse_lazy("tcn:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "accounts/password/reset/done/",
        auth.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/password/reset/<uidb64>/<token>/",
        auth.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("tcn:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password/reset/complete/",
        auth.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]


urlpatterns = [
    path("feeds/", include("tcn.apps.feeds.urls")),
    path("l/<slug:slug>/", views.LinkRedirectView.as_view(), name="redirect"),
    *auth_urls,
    path("authors/", views.UserListView.as_view(), name="authors"),
    path("authors/<slug:slug>/", views.UserDetailView.as_view(), name="author"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("articles/", views.ArticleListView.as_view(), name="articles"),
    path(
        "articles/following/",
        views.FollowingArticleListView.as_view(),
        name="following-articles",
    ),
    path(
        "articles/saved/", views.SavedArticleListView.as_view(), name="saved-articles"
    ),
    path("articles/archive/", views.ArticleArchiveView.as_view(), name="archive"),
    path("articles/<int:year>/", views.ArticleYearView.as_view(), name="articles-y"),
    path(
        "articles/<int:year>/<int:month>/",
        views.ArticleMonthView.as_view(),
        name="articles-m",
    ),
    path(
        "articles/<int:year>/<int:month>/<int:day>/",
        views.ArticleDayView.as_view(),
        name="articles-d",
    ),
    path(
        "articles/<int:year>/<int:month>/<int:day>/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article",
    ),
]
