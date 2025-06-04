"""API endpoints for al_yaqeen.articles"""

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from al_yaqeen.articles.models import Article
from al_yaqeen.articles.serializers import ArticleSerializer
from al_yaqeen.mixins.views import ActionPermissionsMixin, ActionSerializersMixin
from al_yaqeen.permissions import IsOwner
from al_yaqeen.reactions.serializers import ReactionSerializer


# Create your views here.
class ArticleViewSet(ActionSerializersMixin, ActionPermissionsMixin, ModelViewSet):
    """
    # Articles API documentation

    This document outlines how to use `Articles API` for managing user data.
    All endpoints are available under `/api/articles` and require token authentication
    unless noted otherwise.

    > **Note:** Replace `YOUR_TOKEN` with a valid authentication token.

    ---

    ## Standard Endpoints

    ### 1. List Articles

    - **Method:** `GET`  
    - **Endpoint:** `/api/articles`  
    - **Description:** Retrieves a list of all articles. Supports searching, filtering, and ordering.

    #### Query Parameters

    - **Search:**  
    - Parameter: `search`  
    - Fields: `title`, `headline`, `content`  
    - Example:  

        ```
        ?search=breaking
        ```

    - **Filtering:**  
    - Fields: `owner`, `category`, `is_breaking`  
    - Example:  

        ```
        ?category=Sports&is_breaking=true
        ```

    - **Ordering:**  
    - Field Options: `title`, `created_at`, `updated_at`  
    - Example:  

        ```
        ?ordering=-created_at
        ```

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/articles?search=python&ordering=-created_at \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A paginated JSON list of articles, for example:

    ```json
    [
        {
            "id": 10,
            "title": "Python Tips and Tricks",
            "headline": "Improve your Python code...",
            "content": "Full article content here...",
            "owner": 2,
            "category": "Programming",
            "is_breaking": false,
            "created_at": "2025-05-30T12:34:56Z",
            "updated_at": "2025-05-31T08:22:33Z"
        },
        ...
    ]
    ```

    ---

    ### 2. Retrieve an Article

    - **Method:** `GET`  
    - **Endpoint:** `/api/articles/{id}`  
    - **Description:** Retrieves details for a specific article by its ID.

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/articles/10 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    ```json
    {
        "id": 10,
        "title": "Python Tips and Tricks",
        "headline": "Improve your Python code...",
        "content": "Full article content here...",
        "owner": 2,
        "category": "Programming",
        "is_breaking": false,
        "created_at": "2025-05-30T12:34:56Z",
        "updated_at": "2025-05-31T08:22:33Z"
    }
    ```

    ---

    ### 3. Create an Article

    - **Method:** `POST`  
    - **Endpoint:** `/api/articles`  
    - **Description:** Creates a new article. The authenticated user is automatically assigned as the article's owner.

    #### Usage Example (cURL)

    ```bash
    curl -X POST /api/articles \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{
                "title": "New Developments in AI",
                "headline": "AI breakthroughs you should know about",
                "content": "Full details on the latest in AI...",
                "category": "Technology",
                "is_breaking": true
            }'
    ```

    #### Expected Response

    A JSON object representing the newly created article.

    ---

    ### 4. Update an Article

    - **Method:** `PATCH` (partial update) or `PUT` (full update)  
    - **Endpoint:** `/api/articles/{id}`  
    - **Description:** Updates an existing article.

    #### Usage Example (cURL)

    ```bash
    curl -X PATCH /api/articles/10 \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{"headline": "Updated Headline for the Article"}'
    ```

    #### Expected Response

    A JSON object showing the updated article details.

    ---

    ### 5. Delete an Article

    - **Method:** `DELETE`  
    - **Endpoint:** `/api/articles/{id}`  
    - **Description:** Deletes the specified article.

    #### Usage Example (cURL)

    ```bash
    curl -X DELETE /api/articles/10 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    HTTP status 204 (No Content).

    ---

    ## Extra Actions

    ### 1. React to an Article

    - **Method:** `POST`  
    - **Endpoint:** `/api/articles/{id}/react`  
    - **Description:** Toggle a reaction (e.g., an emoji) on an article. If you have not yet reacted, the reaction will be added; if you have, it will be removed.

    #### Usage Example (cURL)

    ```bash
    curl -X POST /api/articles/10/react \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{"emoji": "👍"}'
    ```

    #### Expected Response

    A JSON object containing a details message, for example:

    ```json
    {
        "details": "You reacted to 'Python Tips and Tricks' with 👍"
    }
    ```

    ---

    ### 2. Star an Article

    - **Method:** `POST`  
    - **Endpoint:** `/api/articles/{id}/star`  
    - **Description:** Toggle starring for an article. Star it if it isn’t starred yet, or un-star it if it already is.

    #### Usage Example (cURL)

    ```bash
    curl -X POST /api/articles/10/star \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A JSON object with a details message, for example:

    ```json
    {
        "details": "Article 'Python Tips and Tricks' starred"
    }
    ```

    ---

    ### 3. Popular Articles

    - **Method:** `GET`  
    - **Endpoint:** `/api/articles/popular`  
    - **Description:** Retrieves articles ordered by popularity (i.e., by the number of stargazers).

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/articles/popular \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A paginated JSON list of articles sorted by popularity.

    ---

    ### 4. Trending Articles

    - **Method:** `GET`  
    - **Endpoint:** `/api/articles/trending`  
    - **Description:** Retrieves articles that are trending. (Articles returned have been filtered based on a creation date criterion.)

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/articles/trending \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A paginated JSON list of trending articles.

    ---

    ### 5. Starred Articles

    - **Method:** `GET`  
    - **Endpoint:** `/api/articles/starred`  
    - **Description:** Retrieves articles that the authenticated user has starred.

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/articles/starred \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A paginated JSON list of articles starred by the current user.

    ---

    ## Authentication

    For all endpoints that require authentication, include the following header:

    ```
    Authorization: Token YOUR_TOKEN
    ```
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    search_fields = ["title", "headline", "content"]
    filterset_fields = ["owner", "category", "is_breaking"]
    ordering_fields = ["title", "created_at", "updated_at"]
    action_serializers = {
        "default": serializer_class,
        "star": Serializer,
        "react": ReactionSerializer,
    }
    action_permissions = {
        "default": permission_classes,
        "list": permission_classes[:1],
        "retrieve": permission_classes[:1],
        "react": permission_classes[:1],
        "star": permission_classes[:1],
    }

    def perform_create(self, serializer):
        """Save the object with owner"""

        serializer.save(owner=self.request.user)

    @action(methods=["post"], detail=True)
    def react(self, request: Request, pk: int) -> Response:
        """React to an article"""

        message: str

        # Get article object
        article = self.get_object()

        # Data validation
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(
                serializer.error_messages,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.request.user not in article.reactions.all():
            article.reactions.add(self.request.user)
            message = f"You reacted to {article} with {serializer.validated_data.get('emoji')}"

        else:
            article.reactions.remove(self.request.user)
            message = f"You un-reacted to {article}"

        return Response({"details": message}, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def star(self, request: Request, pk: int) -> Response:
        """Star an article"""

        message: str

        # Get article object
        article = self.get_object()

        # Data validation
        serializer = self.get_serializer(data=request.POST)

        if not serializer.is_valid():
            return Response(
                serializer.error_messages,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.request.user not in article.stargazers.all():
            article.stargazers.add(self.request.user)
            message = f"Article {article} starred"

        else:
            article.stargazers.remove(self.request.user)
            message = f"Article {article} un-starred"

        return Response({"details": message}, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def popular(self, request: Request) -> Response:
        """Popular articles"""

        # Get queryset and filter
        queryset = self.filter_queryset(self.get_queryset()).order_by("-stargazers")

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Return the data
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def trending(self, request: Request) -> Response:
        """Trending articles"""

        # Get queryset and filter
        queryset = self.filter_queryset(self.get_queryset()).filter(
            created_at__gt=timezone.now()
        )

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Return the data
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def starred(self, request: Request) -> Response:
        """Starred articles"""

        # Get queryset and filter
        queryset = self.filter_queryset(self.get_queryset()).filter(
            stargazers=request.user
        )

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Return the data
        return Response(serializer.data)
