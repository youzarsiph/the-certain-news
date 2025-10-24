"""Tests for tcn.ui"""

from tcn import APP_NAME

# Constants
USERS = {
    "user": {
        "username": "user",
        "email": "user@tests.com",
        "password": "user.tests.1234",
        "slug": "user",
    },
    "writer": {
        "username": "writer",
        "email": "writer@tests.com",
        "password": "writer.tests.1234",
        "slug": "writer",
    },
}

URL_PATTERNS = {
    "auth": {
        "public": {
            f"{APP_NAME}:login": [],
            f"{APP_NAME}:subscribe": [],
            f"{APP_NAME}:password_reset": [],
            f"{APP_NAME}:password_reset_done": [],
            f"{APP_NAME}:password_reset_complete": [],
        },
        "authenticated": {
            f"{APP_NAME}:profile": [],
            f"{APP_NAME}:u-user": [USERS["user"]["slug"]],
            f"{APP_NAME}:d-user": [USERS["user"]["slug"]],
            f"{APP_NAME}:password_change": [],
            f"{APP_NAME}:password_change_done": [],
            f"{APP_NAME}:password_reset_confirm": ["uidb64", "token"],
        },
    },
    "public": {
        "atom-latest": [],
        "atom-breaking": [],
        "rss-latest": [],
        "rss-breaking": [],
        "author": [USERS["user"]["slug"]],
        "authors": [],
        "search": [],
        "articles": [],
        "following-articles": [],
        "saved-articles": [],
        "archive": [],
        "articles-y": [2025],
        "articles-m": [2025, 1],
        "articles-d": [2025, 1, 1],
        # The following 2 test require the existence of an article
        # "article": [2025, 1, 1, "slug"],
        # "redirect": ["slug"],
    },
}
