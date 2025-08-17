"""URL Configuration for tcn.api"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

from tcn.api.viewsets.comments import CommentViewSet
from tcn.api.viewsets.reactions import ReactionViewSet
from tcn.api.viewsets.users import UserViewSet

# Create your URLConf here.
router = DefaultRouter()
router.register("comments", CommentViewSet, "comment")
router.register("reactions", ReactionViewSet, "reaction")
router.register("users", UserViewSet, "user")

# Wagtail APIs
api_router = WagtailAPIRouter("wagtail-api")
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", api_router.urls),
]
