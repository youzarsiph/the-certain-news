"""API endpoints for tcn.apps.comments"""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tcn.api.mixins import ActionPermissionsMixin, OwnerFilterMixin
from tcn.api.permissions import DenyAll, IsOwner
from tcn.api.serializers.comments import CommentSerializer
from tcn.apps.comments.models import Comment


# Create your views here.
class BaseCommentVS(ActionPermissionsMixin, ModelViewSet):
    """Base viewset for extension"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    search_fields = ["content"]
    filterset_fields = ["owner", "article"]
    ordering_fields = ["created_at", "updated_at"]
    action_permissions = {"default": permission_classes}

    @action(methods=["post"], detail=True)
    def reply(self, request: Request, pk: int) -> Response:
        """Reply to a comment"""

        # Get comment object
        comment = self.get_object()

        # Validate and save comment
        serializer = CommentSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=False):
            reply = serializer.save(owner=request.user, article=comment.article)

            # Add comment to replies
            comment.replies.add(reply)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(OwnerFilterMixin, BaseCommentVS):
    """
    # Comments API Documentation

    The Comment API enables users to create, view, update, and delete comments,
    as well as reply to existing comments. Comments support advanced query options for improved content retrieval.

    ---

    ## Standard Endpoints

    ### 1. List Comments

    - **Method:** `GET`  
    - **Endpoint:** `/api/comments`  
    - **Description:**  
    Retrieves a paginated list of all comments. Supports advanced querying.

    #### Query Parameters

    - **Search:**  
    - **Parameter:** `search`  
    - **Field Searched:** `content`  
    - **Example:**  

        ```
        ?search=awesome
        ```

    - **Filtering:**  
    - **Fields:** `user`, `article`  
    - **Example:**  

        ```
        ?owner=3&article=12
        ```

    - **Ordering:**  
    - **Parameter:** `ordering`  
    - **Available Fields:** `created_at`, `updated_at`  
    - **Example:**  

        ```
        ?ordering=-created_at
        ```

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/comments?search=awesome&ordering=-created_at \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A JSON list (or paginated response) of comment objects similar to:

    ```json
    [
        {
            "id": 15,
            "content": "This article was awesome!",
            "user": 3,
            "article": 12,
            "created_at": "2025-06-02T10:20:30Z",
            "updated_at": "2025-06-02T10:20:30Z"
        },
        ...
    ]
    ```

    ---

    ### 2. Retrieve a Comment

    - **Method:** `GET`  
    - **Endpoint:** `/api/comments/{id}` (replace `{id}` with the actual comment ID)  
    - **Description:**  
    Returns detailed information for a specific comment.

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/comments/15 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    ```json
    {
        "id": 15,
        "content": "This article was awesome!",
        "user": 3,
        "article": 12,
        "created_at": "2025-06-02T10:20:30Z",
        "updated_at": "2025-06-02T10:20:30Z"
    }
    ```

    ---

    ### 3. Update a Comment

    - **Method:** `PATCH` or `PUT`  
    - **Endpoint:** `/api/comments/{id}` (replace `{id}` with the comment's ID)  
    - **Description:**  
    Updates the specified comment. Only the owner is permitted to update it.

    #### Usage Example (cURL - PATCH)

    ```bash
    curl -X PATCH /api/comments/15 \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{"content": "Updated comment content."}'
    ```

    #### Expected Response

    A JSON object with the updated comment details:

    ```json
    {
        "id": 15,
        "content": "Updated comment content.",
        "user": 3,
        "article": 12,
        "created_at": "2025-06-02T10:20:30Z",
        "updated_at": "2025-06-02T11:15:00Z"
    }
    ```

    ---

    ### 4. Delete a Comment

    - **Method:** `DELETE`  
    - **Endpoint:** `/api/comments/{id}` (replace `{id}` with the comment's ID)  
    - **Description:**  
    Deletes the specified comment. Only the owner can delete their comment.

    #### Usage Example (cURL)

    ```bash
    curl -X DELETE /api/comments/15 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    HTTP status 204 (No Content) is returned on successful deletion.

    ---

    ## Extra Action

    ### Reply to a Comment

    - **Method:** `POST`  
    - **Endpoint:** `/api/comments/{id}/reply` (replace `{id}` with the parent comment's ID)  
    - **Description:**  
    Allows a user to reply to an existing comment. The new reply is created as a comment and linked to the original comment.

    #### Usage Example (cURL)

    ```bash
    curl -X POST /api/comments/15/reply \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{
                "content": "Thanks for your insight!"
            }'
    ```

    #### Expected Response

    A JSON object representing the newly created reply:

    ```json
    {
        "id": 17,
        "content": "Thanks for your insight!",
        "user": 3,
        "article": 12,
        "created_at": "2025-06-02T11:30:00Z",
        "updated_at": "2025-06-02T11:30:00Z"
    }
    ```

    The reply action attaches the new comment to the parent comment's replies list.

    ---

    ## Authentication

    For all endpoints that require authentication, include your token in the Authorization header:

    ```
    Authorization: Token YOUR_TOKEN
    ```
    """

    action_permissions = {**BaseCommentVS.action_permissions, "create": [DenyAll]}


class ArticleComments(BaseCommentVS):
    """
    # Comments API Documentation

    The Comment API enables users to create, view, update, and delete comments,
    as well as reply to existing comments. Comments support advanced query options for improved content retrieval.

    ---

    ## Standard Endpoints

    ### 1. List Comments

    - **Method:** `GET`  
    - **Endpoint:** `/api/comments`  
    - **Description:**  
    Retrieves a paginated list of all comments. Supports advanced querying.

    #### Query Parameters

    - **Search:**  
    - **Parameter:** `search`  
    - **Field Searched:** `content`  
    - **Example:**  

        ```
        ?search=awesome
        ```

    - **Filtering:**  
    - **Fields:** `user`, `article`  
    - **Example:**  

        ```
        ?owner=3&article=12
        ```

    - **Ordering:**  
    - **Parameter:** `ordering`  
    - **Available Fields:** `created_at`, `updated_at`  
    - **Example:**  

        ```
        ?ordering=-created_at
        ```

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/comments?search=awesome&ordering=-created_at \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A JSON list (or paginated response) of comment objects similar to:

    ```json
    [
        {
            "id": 15,
            "content": "This article was awesome!",
            "user": 3,
            "article": 12,
            "created_at": "2025-06-02T10:20:30Z",
            "updated_at": "2025-06-02T10:20:30Z"
        },
        ...
    ]
    ```

    ---

    ### 2. Retrieve a Comment

    - **Method:** `GET`  
    - **Endpoint:** `/api/comments/{id}` (replace `{id}` with the actual comment ID)  
    - **Description:**  
    Returns detailed information for a specific comment.

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/comments/15 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    ```json
    {
        "id": 15,
        "content": "This article was awesome!",
        "user": 3,
        "article": 12,
        "created_at": "2025-06-02T10:20:30Z",
        "updated_at": "2025-06-02T10:20:30Z"
    }
    ```

    ---

    ### 3. Create a New Comment

    - **Method:** `POST`  
    - **Endpoint:** `/api/comments`  
    - **Description:**  
    Creates a new comment. The authenticated user is automatically set as the comment’s owner.

    #### Usage Example (cURL)

    ```bash
    curl -X POST /api/comments \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{
                "content": "I really enjoyed this article.",
                "article": 12
            }'
    ```

    #### Expected Response

    A JSON object representing the newly created comment:

    ```json
    {
        "id": 16,
        "content": "I really enjoyed this article.",
        "user": 3,
        "article": 12,
        "created_at": "2025-06-02T11:00:00Z",
        "updated_at": "2025-06-02T11:00:00Z"
    }
    ```

    ---

    ### 4. Update a Comment

    - **Method:** `PATCH` or `PUT`  
    - **Endpoint:** `/api/comments/{id}` (replace `{id}` with the comment's ID)  
    - **Description:**  
    Updates the specified comment. Only the owner is permitted to update it.

    #### Usage Example (cURL - PATCH)

    ```bash
    curl -X PATCH /api/comments/15 \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{"content": "Updated comment content."}'
    ```

    #### Expected Response

    A JSON object with the updated comment details:

    ```json
    {
        "id": 15,
        "content": "Updated comment content.",
        "user": 3,
        "article": 12,
        "created_at": "2025-06-02T10:20:30Z",
        "updated_at": "2025-06-02T11:15:00Z"
    }
    ```

    ---

    ### 5. Delete a Comment

    - **Method:** `DELETE`  
    - **Endpoint:** `/api/comments/{id}` (replace `{id}` with the comment's ID)  
    - **Description:**  
    Deletes the specified comment. Only the owner can delete their comment.

    #### Usage Example (cURL)

    ```bash
    curl -X DELETE /api/comments/15 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    HTTP status 204 (No Content) is returned on successful deletion.

    ---

    ## Extra Action

    ### Reply to a Comment

    - **Method:** `POST`  
    - **Endpoint:** `/api/comments/{id}/reply` (replace `{id}` with the parent comment's ID)  
    - **Description:**  
    Allows a user to reply to an existing comment. The new reply is created as a comment and linked to the original comment.

    #### Usage Example (cURL)

    ```bash
    curl -X POST /api/comments/15/reply \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{
                "content": "Thanks for your insight!"
            }'
    ```

    #### Expected Response

    A JSON object representing the newly created reply:

    ```json
    {
        "id": 17,
        "content": "Thanks for your insight!",
        "user": 3,
        "article": 12,
        "created_at": "2025-06-02T11:30:00Z",
        "updated_at": "2025-06-02T11:30:00Z"
    }
    ```

    The reply action attaches the new comment to the parent comment's replies list.

    ---

    ## Authentication

    For all endpoints that require authentication, include your token in the Authorization header:

    ```
    Authorization: Token YOUR_TOKEN
    ```
    """

    def perform_create(self, serializer):
        """Add article to comment automatically"""

        serializer.save(
            user_id=self.request.user.pk, article_id=self.kwargs["article_id"]
        )

    def get_queryset(self):
        """Filter queryset by article"""

        return super().get_queryset().filter(article_id=self.kwargs["article_id"])
