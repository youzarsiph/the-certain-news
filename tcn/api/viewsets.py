"""API endpoints for tcn.apps.users"""

from django.utils.translation import gettext_lazy as _, get_language_from_request
from djoser.views import UserViewSet as BaseUVS
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from tcn.api.serializers import ArticleSerializer
from tcn.apps.articles.models import Article


# Create your views here.
class UserViewSet(BaseUVS):
    """
    API endpoints for managing user accounts.

    ## Overview

    API endpoints are to manage user registration, authentication, and profile operations.
    Custom endpoints and extra actions have been added to support additional user-related features.

    ## Endpoints

    - **List Users**
    `GET /api/users`
    Retrieves a list of all user accounts.

    - **Create User (Registration)**
    `POST /api/users`
    Registers a new user. Requires user details such as username, email, and password.

    - **Retrieve User**
    `GET /api/users/{id}`
    Retrieves detailed information for the user account identified by `id`.

    - **Update User**
    `PUT /api/users/{id}`
    Fully updates the user account with the provided data.

    - **Partial Update User**
    `PATCH /api/users/{id}`
    Partially updates the user account fields.

    - **Delete User**
    `DELETE /api/users/{id}`
    Deletes the user account identified by `id`.

    ## Query Parameters

    - **search:**
    Filter users by username, first name, or last name (e.g., `?search=john`).

    - **ordering:**
    Order users by a specific field (e.g., `?ordering=-date_joined` for the most recent first).

    ## Permissions

    - **Authenticated Users:**
    Can view their own profile details.

    - **Admin/Staff Users:**
    Can list, retrieve, update, or delete any user account.

    *Note: Some endpoints (like registration) might be public while others require authentication.*

    ## Extra Actions

    This viewset extends functionality beyond the standard endpoints with additional custom actions:

    ## Example API Requests

    **List Users:**

    ```bash
    curl -X GET /api/users \\
        -H "Authorization: Bearer YOUR_TOKEN_HERE"
    ```

    **Register a New User:**

    ```bash
    curl -X POST /api/users \\
        -H "Content-Type: application/json" \\
        -d '{
                "username": "johndoe",
                "email": "john@example.com",
                "password": "securepassword"
            }'
    ```

    **Set User Password:**
    
    ```bash
    curl -X POST /api/users/1/set_password \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Bearer YOUR_TOKEN_HERE" \\
        -d '{
                "old_password": "oldpassword",
                "new_password": "newsecurepassword"
            }'
    ```
    
    **Follow a Writer:**

    ```bash
    curl -X POST /api/users/{slug}/follow \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Bearer YOUR_TOKEN_HERE"
    ```
    """

    lookup_field = "slug"
    search_fields = ["username", "first_name", "last_name"]
    ordering_fields = ["username", "date_joined", "last_login"]
    filterset_fields = ["username"]

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="follow",
        url_name="follow",
    )
    def follow(self, request: Request, slug: str, *args, **kwargs) -> Response:
        """
        Follow a writer

        Args:
            request (Request): The request object containing user data.
            slug (str): The slug of the writer to follow.

        Returns:
            Response: A response indicating success or failure of the operation.
        """

        user = self.get_object()

        if request.user.following.contains(user):
            request.user.following.remove(user)
            message = _(f"You are no longer following {user.username}.")

        else:
            request.user.following.add(user)
            message = _(f"You are following {user.username}.")

        return Response({"detail": message}, status=status.HTTP_200_OK)


class ArticleViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows articles to be viewed.
    """

    lookup_field = "slug"
    queryset = Article.objects.live().public().prefetch_related("locale")
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def get_queryset(self):
        """Filter queryset by language"""

        return (
            super()
            .get_queryset()
            .filter(
                locale__language_code=get_language_from_request(
                    self.request,
                    check_path=True,
                )
            )
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="save",
        url_name="save",
    )
    def save(self, request: Request, slug: str, *args, **kwargs) -> Response:
        """
        Save an article

        Args:
            request (Request): The request object containing user data.
            slug (str): The slug of the article to save.

        Returns:
            Response: A response indicating success or failure of the operation.
        """

        article = self.get_object()

        if request.user.bookmarked_articles.contains(article):
            request.user.bookmarked_articles.remove(article)
            message = _("Article removed from your saved list.")

        else:
            request.user.bookmarked_articles.add(article)
            message = _("Article added to your saved list.")

        return Response({"detail": message}, status=status.HTTP_200_OK)
