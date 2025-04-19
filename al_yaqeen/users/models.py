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
- followers: User followers

Methods:
- article_count: Number of articles of a user
- follower_count: Number of followers of a user
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """Al_yaqeen Users"""

    photo = models.ImageField(
        null=True,
        blank=True,
        help_text="User photo",
        upload_to="al_yaqeen/images/users/",
    )
    cover = models.ImageField(
        null=True,
        blank=True,
        help_text="User cover",
        upload_to="al_yaqeen/images/covers/",
    )
    bio = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="User bio",
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="followers.Follower",
        help_text="User followers",
    )

    @property
    def article_count(self) -> int:
        """Number of articles of a user"""

        return self.articles.count()

    @property
    def follower_count(self) -> int:
        """Number of followers of a user"""

        return self.followers.count()
