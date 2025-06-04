"""API endpoints for al_yaqeen.users"""

from djoser.views import UserViewSet as BaseUVS


class UserViewSet(BaseUVS):
    """
    # Users API Documentation

    This document outlines how to use `Users API` for managing user data.
    All endpoints are available under `/api/users` and require token authentication
    unless noted otherwise.

    > **Note:** Replace `YOUR_TOKEN` with a valid authentication token.

    ---

    ## Standard Endpoints

    ### 1. List Users

    - **Method:** `GET`  
    - **URL:** `/api/users`  
    - **Description:** Retrieves a list of all registered users.
    
    **Usage Example (cURL):**

    ```bash
    curl -X GET /api/users \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    **Expected Response:**

    ```json
    [
        {
            "id": 1,
            "username": "johndoe",
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe"
        },
        {
            "id": 2,
            "username": "janedoe",
            "email": "janedoe@example.com",
            "first_name": "Jane",
            "last_name": "Doe"
        }
    ]
    ```

    ---

    ### 2. Retrieve a User

    - **Method:** `GET`  
    - **URL:** `/api/users/{id}` (replace `{id}` with the user ID)  
    - **Description:** Retrieves details for a specific user.
    
    **Usage Example (cURL):**

    ```bash
    curl -X GET /api/users/1 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    **Expected Response:**

    ```json
    {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    ```

    ---

    ### 3. Create a New User

    - **Method:** `POST`  
    - **URL:** `/api/users`  
    - **Description:** Creates a new user account.
    
    **Usage Example (cURL):**

    ```bash
    curl -X POST /api/users \\
    -H "Content-Type: application/json" \\
    -d '{
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
            "first_name": "New",
            "last_name": "User"
        }'
    ```

    **Expected Response:**

    ```json
    {
        "id": 3,
        "username": "newuser",
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User"
    }
    ```

    ---

    ### 4. Update a User

    - **Method:** `PATCH`  
    - **URL:** `/api/users/{id}` (replace `{id}` with the user ID)  
    - **Description:** Updates information for a specific user.
    
    **Usage Example (cURL):**

    ```bash
    curl -X PATCH /api/users/1 \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -H "Content-Type: application/json" \\
        -d '{
                "first_name": "Johnny",
                "last_name": "Doe"
            }'
    ```

    **Expected Response:**

    ```json
    {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "first_name": "Johnny",
        "last_name": "Doe"
    }
    ```

    ---

    ### 5. Delete a User

    - **Method:** `DELETE`  
    - **URL:** `/api/users/{id}` (replace `{id}` with the user ID)  
    - **Description:** Deletes the specified user account.
    
    **Usage Example (cURL):**

    ```bash
    curl -X DELETE /api/users/1 \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    **Expected Response:**  
    HTTP 204 No Content

    ---

    ## Extra Actions

    ### 1. Retrieve Current User Profile

    - **Method:** `GET`  
    - **URL:** `/api/users/me`  
    - **Description:** Returns the profile of the currently authenticated user.
    
    **Usage Example (cURL):**

    ```bash
    curl -X GET /api/users/me \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    **Expected Response:**

    ```json
    {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    ```

    ---

    ### 2. Change Password

    - **Method:** `POST`  
    - **URL:** `/api/users/{id}/set_password` (replace `{id}` with the user ID)  
    - **Description:** Changes the user's password.
    
    **Usage Example (cURL):**

    ```bash
    curl -X POST /api/users/1/set_password \\
        -H "Authorization: Token YOUR_TOKEN" \\
        -H "Content-Type: application/json" \\
        -d '{
                "old_password": "oldpass123",
                "new_password": "newpass456"
            }'
    ```

    **Expected Response:**

    ```json
    {
        "status": "success",
        "message": "Password changed successfully."
    }
    ```

    ---

    ### 3. Resend Activation Email

    - **Method:** `POST`  
    - **URL:** `/api/users/resend_activation`  
    - **Description:** Resends the account activation email.
    
    **Usage Example (cURL):**

    ```bash
    curl -X POST /api/users/resend_activation \\
        -H "Content-Type: application/json" \\
        -d '{
                "email": "johndoe@example.com"
            }'
    ```

    **Expected Response:**

    ```json
    {
        "status": "success",
        "message": "Activation email resent."
    }
    ```

    ---

    ## Searching, Filtering, and Ordering

    The `UserViewSet` supports advanced query features to help you narrow down user results efficiently.
    Below are the details of the enabled query parameters:

    ### **Search**

    - **Fields:** `username`, `first_name`, `last_name`
    - **Usage:** Add a `search` parameter in the query string to search across the specified fields.
    
    **Example:**

    ```bash
    curl -X GET /api/users?search=johndoe \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    ### **Filtering**

    - **Fields:** `username`, `is_staff`
    - **Usage:** Specify one or more of these fields directly in the query string to filter results.
    
    **Examples:**

    ```bash
    # Filter by username
    curl -X GET /api/users?username=johndoe \\
        -H "Authorization: Token YOUR_TOKEN"

    # Filter by staff status (True/False)
    curl -X GET /api/users?is_staff=True \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    ### **Ordering**

    - **Fields:** `username`, `date_joined`, `last_login`
    - **Usage:** Use the `ordering` parameter to sort the results.  
    Prepend a field with a hyphen (`-`) to indicate descending order.
    
    **Examples:**

    ```bash
    # Order by username (ascending)
    curl -X GET /api/users?ordering=username \\
        -H "Authorization: Token YOUR_TOKEN"

    # Order by date joined (descending)
    curl -X GET /api/users?ordering=-date_joined \\
        -H "Authorization: Token YOUR_TOKEN"
    ```

    ---

    ## Authentication

    For endpoints that require authentication, include your token in the `Authorization` header as follows:

    ```
    Authorization: Token YOUR_TOKEN
    ```
    """

    lookup_field = "pk"
    search_fields = ["username", "first_name", "last_name"]
    ordering_fields = ["username", "date_joined", "last_login"]
    filterset_fields = ["username", "is_staff"]
