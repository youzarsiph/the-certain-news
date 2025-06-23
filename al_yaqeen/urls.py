"""URLConf for al_yaqeen"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from al_yaqeen.articles.views import ArticleViewSet
from al_yaqeen.categories.views import CategoryViewSet
from al_yaqeen.comments.views import CommentViewSet
from al_yaqeen.reactions.views import ReactionViewSet
from al_yaqeen.users.views import UserViewSet

# Create your URLConf here.
router = DefaultRouter(trailing_slash=False)
router.register("articles", ArticleViewSet, "article")
router.register("categories", CategoryViewSet, "category")
router.register("comments", CommentViewSet, "comment")
router.register("reactions", ReactionViewSet, "reaction")
router.register("users", UserViewSet, "user")

urlpatterns = [
    path("", include(router.urls)),
]
