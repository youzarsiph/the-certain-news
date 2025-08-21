"""Data Models for tcn.apps.links"""

from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


def create_slug() -> str:
    return token_urlsafe(8)


User = get_user_model()


# Create your models here.
class Link(models.Model):
    """Shortened links"""

    article = models.OneToOneField(
        "articles.Article",
        on_delete=models.CASCADE,
        related_name="link",
        help_text=_("article"),
        verbose_name=_("Related article"),
    )
    slug = models.SlugField(
        max_length=16,
        unique=True,
        db_index=True,
        default=create_slug,
        help_text=_("slug"),
        verbose_name=_("Link url"),
    )
    views = models.ManyToManyField(
        User,
        related_name="views",
        help_text=_("views"),
        verbose_name=_("Article views"),
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text=_("views"),
        verbose_name=_("Article views"),
    )

    class Meta:
        """Meta data"""

        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def __str__(self) -> str:
        return self.article.title
