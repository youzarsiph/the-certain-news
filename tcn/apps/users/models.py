"""Data Models for tcn.apps.users"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from tcn.apps.articles.models import Article


# Create your models here.
class User(AbstractUser):
    """Users"""

    slug = models.SlugField(
        unique=True,
        db_index=True,
        allow_unicode=True,
        verbose_name=_("slug"),
        help_text=_("Letters, numbers and dash only"),
    )
    country = CountryField(
        null=True,
        blank=True,
        verbose_name=_("country"),
        help_text=_("User country"),
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name=_("phone number"),
        help_text=_("User phone number"),
    )
    photo = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_("image"),
        upload_to="images/users/",
        help_text=_("Profile image"),
    )
    bio = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_("bio"),
        help_text=_("Tell us about yourself"),
    )
    bookmarked_articles = models.ManyToManyField(
        "articles.Article",
        blank=True,
        related_name="bookmarked_by",
        verbose_name=_("bookmarked articles"),
        help_text=_("Articles bookmarked by user"),
    )
    followers = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="following",
        verbose_name=_("followers"),
        help_text=_("Users following this user"),
    )

    @property
    def article_count(self) -> int:
        """Return the number of articles authored by the user"""

        return Article.objects.live().public().filter(owner=self).count()
