"""API endpoints for tcn.apps.reactions"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tcn.api.mixins import ActionPermissionsMixin
from tcn.api.permissions import DenyAll, IsOwner
from tcn.api.serializers.reactions import ReactionSerializer
from tcn.apps.reactions.models import Reaction
from tcn.ui.mixins import UserFilterMixin


# Create your views here.
class BaseReactionVS(ActionPermissionsMixin, ModelViewSet):
    """Base view set for extension"""

    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    search_fields = ["emoji"]
    filterset_fields = ["owner", "article", "emoji"]
    ordering_fields = ["created_at", "updated_at"]
    action_permissions = {"default": permission_classes}


class ReactionViewSet(UserFilterMixin, BaseReactionVS):
    """
    # Reactions API Documentation

    The Reaction API enables users to interact with reaction objects (such as emoji reactions) on articles.
    Standard RUD operations are supported along with advanced query features to search, filter, and order reactions.

    ---

    ## Standard Endpoints

    ### 1. List Reactions

    - **Method:** `GET`  
    - **Endpoint:** `/api/reactions`  
    - **Description:**  
    Retrieves a paginated list of all reactions. Supports searching by emoji, filtering by user, article, and emoji, and ordering by creation or update times.

    #### Query Parameters

    - **Search:**  
    - **Parameter:** `search`  
    - **Field Searched:** `emoji`  
    - **Example:**  

        ```
        ?search=👍
        ```

    - **Filtering:**  
    - **Parameters:**  
        - `owner` (to filter by user ID)  
        - `article` (to filter by article ID)  
        - `emoji` (to filter by a specific emoji value)  
    - **Example:**  

        ```
        ?owner=5&emoji=❤️
        ```

    - **Ordering:**  
    - **Parameter:** `ordering`  
    - **Fields Available:** `created_at`, `updated_at`  
    - To order in descending order, prepend the field with a hyphen.  
    - **Example:**  

        ```
        ?ordering=-created_at
        ```

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/reactions?search=👍&ordering=-created_at \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A JSON list (or paginated response) of reaction objects, for example:

    ```json
    [
        {
            "id": 101,
            "emoji": "👍",
            "user": 5,
            "article": 12,
            "created_at": "2025-06-02T10:20:30Z",
            "updated_at": "2025-06-02T10:20:30Z"
        },
        {
            "id": 102,
            "emoji": "😊",
            "user": 7,
            "article": 12,
            "created_at": "2025-06-02T11:00:00Z",
            "updated_at": "2025-06-02T11:00:00Z"
        }
    ]
    ```

    ---

    ### 2. Retrieve a Reaction

    - **Method:** `GET`  
    - **Endpoint:** `/api/reactions/{id}` (replace `{id}` with the reaction's ID)  
    - **Description:**  
    Retrieves detailed information for a specific reaction.

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/reactions/101 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    ```json
    {
        "id": 101,
        "emoji": "👍",
        "user": 5,
        "article": 12,
        "created_at": "2025-06-02T10:20:30Z",
        "updated_at": "2025-06-02T10:20:30Z"
    }
    ```

    ---

    ### 3. Update a Reaction

    - **Method:** `PATCH` (for partial updates) or `PUT` (for full updates)  
    - **Endpoint:** `/api/reactions/{id}` (replace `{id}` with the reaction's ID)  
    - **Description:**  
    Updates a reaction. Only the owner is permitted to update their reactions.
    
    #### Usage Example (Partial Update with PATCH)

    ```bash
    curl -X PATCH /api/reactions/103 \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{"emoji": "😄"}'
    ```

    #### Expected Response

    A JSON object reflecting the updated reaction:

    ```json
    {
        "id": 103,
        "emoji": "😄",
        "user": 5,
        "article": 12,
        "created_at": "2025-06-02T12:30:00Z",
        "updated_at": "2025-06-02T12:45:00Z"
    }
    ```

    ---

    ### 4. Delete a Reaction

    - **Method:** `DELETE`  
    - **Endpoint:** `/api/reactions/{id}` (replace `{id}` with the reaction's ID)  
    - **Description:**  
    Deletes the specified reaction. Only the owner is allowed to delete their reactions.
    
    #### Usage Example (cURL)

    ```bash
    curl -X DELETE /api/reactions/103 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    HTTP status 204 (No Content) is returned on successful deletion.

    ---

    ## Authentication

    Ensure all requests include your authentication token in the request header:

    ```
    Authorization: Token YOUR_TOKEN
    ```
    """

    action_permissions = {**BaseReactionVS.action_permissions, "create": [DenyAll]}


class ArticleReactions(BaseReactionVS):
    """
    # Reactions API Documentation

    The Reaction API enables users to interact with reaction objects (such as emoji reactions) on articles. Standard CRUD operations are supported along with advanced query features to search, filter, and order reactions.

    ---

    ## Standard Endpoints

    ### 1. List Reactions

    - **Method:** `GET`  
    - **Endpoint:** `/api/reactions`  
    - **Description:**  
    Retrieves a paginated list of all reactions. Supports searching by emoji, filtering by user, article, and emoji, and ordering by creation or update times.

    #### Query Parameters

    - **Search:**  
    - **Parameter:** `search`  
    - **Field Searched:** `emoji`  
    - **Example:**  

        ```
        ?search=👍
        ```

    - **Filtering:**  
    - **Parameters:**  
        owner `user` (to filter by user ID)  
        - `article` (to filter by article ID)  
        - `emoji` (to filter by a specific emoji value)  
    - **Example:**  

        ```
        ?owner=5&emoji=❤️
        ```

    - **Ordering:**  
    - **Parameter:** `ordering`  
    - **Fields Available:** `created_at`, `updated_at`  
    - To order in descending order, prepend the field with a hyphen.  
    - **Example:**  

        ```
        ?ordering=-created_at
        ```

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/reactions?search=👍&ordering=-created_at \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    A JSON list (or paginated response) of reaction objects, for example:

    ```json
    [
        {
            "id": 101,
            "emoji": "👍",
            "user": 5,
            "article": 12,
            "created_at": "2025-06-02T10:20:30Z",
            "updated_at": "2025-06-02T10:20:30Z"
        },
        {
            "id": 102,
            "emoji": "😊",
            "user": 7,
            "article": 12,
            "created_at": "2025-06-02T11:00:00Z",
            "updated_at": "2025-06-02T11:00:00Z"
        }
    ]
    ```

    ---

    ### 2. Retrieve a Reaction

    - **Method:** `GET`  
    - **Endpoint:** `/api/reactions/{id}` (replace `{id}` with the reaction's ID)  
    - **Description:**  
    Retrieves detailed information for a specific reaction.

    #### Usage Example (cURL)

    ```bash
    curl -X GET /api/reactions/101 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    ```json
    {
        "id": 101,
        "emoji": "👍",
        "user": 5,
        "article": 12,
        "created_at": "2025-06-02T10:20:30Z",
        "updated_at": "2025-06-02T10:20:30Z"
    }
    ```

    ---

    ### 3. Create a Reaction

    - **Method:** `POST`  
    - **Endpoint:** `/api/reactions`  
    - **Description:**  
    Creates a new reaction. The authenticated user is automatically set as the owner of the reaction.
    
    #### Usage Example (cURL)

    ```bash
    curl -X POST /api/reactions \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{
                "emoji": "❤️",
                "article": 12
            }'
    ```

    #### Expected Response

    A JSON object representing the newly created reaction:

    ```json
    {
        "id": 103,
        "emoji": "❤️",
        "user": 5,
        "article": 12,
        "created_at": "2025-06-02T12:30:00Z",
        "updated_at": "2025-06-02T12:30:00Z"
    }
    ```

    ---

    ### 4. Update a Reaction

    - **Method:** `PATCH` (for partial updates) or `PUT` (for full updates)  
    - **Endpoint:** `/api/reactions/{id}` (replace `{id}` with the reaction's ID)  
    - **Description:**  
    Updates a reaction. Only the owner is permitted to update their reactions.
    
    #### Usage Example (Partial Update with PATCH)

    ```bash
    curl -X PATCH /api/reactions/103 \\
        -H "Content-Type: application/json" \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -d '{"emoji": "😄"}'
    ```

    #### Expected Response

    A JSON object reflecting the updated reaction:

    ```json
    {
        "id": 103,
        "emoji": "😄",
        "user": 5,
        "article": 12,
        "created_at": "2025-06-02T12:30:00Z",
        "updated_at": "2025-06-02T12:45:00Z"
    }
    ```

    ---

    ### 5. Delete a Reaction

    - **Method:** `DELETE`  
    - **Endpoint:** `/api/reactions/{id}` (replace `{id}` with the reaction's ID)  
    - **Description:**  
    Deletes the specified reaction. Only the owner is allowed to delete their reactions.
    
    #### Usage Example (cURL)

    ```bash
    curl -X DELETE /api/reactions/103 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    #### Expected Response

    HTTP status 204 (No Content) is returned on successful deletion.

    ---

    ## Authentication

    Ensure all requests include your authentication token in the request header:

    ```
    Authorization: Token YOUR_TOKEN
    ```
    """

    def perform_create(self, serializer):
        """Add article to reaction automatically"""

        serializer.save(owner=self.request.user, article_id=self.kwargs["article_id"])

    def get_queryset(self):
        """Filter queryset by article"""

        return super().get_queryset().filter(article_id=self.kwargs["article_id"])
