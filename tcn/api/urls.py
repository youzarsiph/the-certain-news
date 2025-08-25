"""URL Configuration for tcn.api"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.contrib.redirects.api import RedirectsAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

from tcn.api.views import ArticleViewSet, CategoryViewSet
from tcn.api.viewsets import UserViewSet

# Create your URLConf here.
router = DefaultRouter()
router.register("users", UserViewSet, "user")

# Wagtail Built-in APIs
api_router = WagtailAPIRouter("wagtail-api")
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
api_router.register_endpoint("redirects", RedirectsAPIViewSet)

# Custom APIs
api_router.register_endpoint("categories", CategoryViewSet)
api_router.register_endpoint("articles", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", api_router.urls),
]
