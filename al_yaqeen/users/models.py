"""
User model

Extends `django.contrib.auth.models.AbstractUser`

Fields:
- username: Username
- email: Email
- first_name: First name
- last_name: Last name
- date_joined: Date joined
- last_login: Last login
- is_active: Designates if the user is active
- is_staff: Designates if the user is staff
- is_superuser: Designates if the user is superuser
- groups: Permission groups
- photo: Profile photo
- cover: Profile cover
- bio: User bio

Methods:
- article_count: Number of articles of a user
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    """Al_yaqeen Users"""

    photo = models.ImageField(
        null=True,
        blank=True,
        help_text=_("User photo"),
        upload_to="al_yaqeen/images/users/",
    )
    bio = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text=_("User bio"),
    )
    saved = models.ManyToManyField(
        "articles.Article",
        blank=True,
        help_text=_("Saved news articles"),
    )

    @property
    def article_count(self) -> int:
        """Number of articles of a user"""

        return self.articles.count()
