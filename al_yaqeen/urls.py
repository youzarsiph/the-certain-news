"""URLConf for al_yaqeen"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from al_yaqeen.articles.views import ArticleViewSet
from al_yaqeen.categories.views import CategoryViewSet
from al_yaqeen.comments.views import CommentViewSet
from al_yaqeen.followers.views import FollowerViewSet
from al_yaqeen.reactions.views import ReactionViewSet
from al_yaqeen.reports.views import ReportViewSet
from al_yaqeen.tags.views import TagViewSet
from al_yaqeen.users.views import UserViewSet


# Create your URLConf here.
router = DefaultRouter(trailing_slash=False)
router.register("articles", ArticleViewSet, "article")
router.register("categories", CategoryViewSet, "category")
router.register("comments", CommentViewSet, "comment")
router.register("followers", FollowerViewSet, "follower")
router.register("reactions", ReactionViewSet, "reaction")
router.register("reports", ReportViewSet, "report")
router.register("tags", TagViewSet, "tag")
router.register("users", UserViewSet, "user")

urlpatterns = [
    path("", include(router.urls)),
]
