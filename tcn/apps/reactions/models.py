"""Reaction model"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from tcn.apps.mixins import DateTimeMixin
from tcn.apps.reactions import REACTIONS

# Create your models here.
User = get_user_model()


class Reaction(DateTimeMixin, models.Model):
    """Article Reactions"""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reactions",
        help_text=_("User"),
    )
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        related_name="reactions",
        help_text=_("Article"),
    )
    emoji = models.CharField(
        max_length=8,
        default="👍🏻",
        choices=REACTIONS,
        help_text=_("Reaction"),
    )

    class Meta:
        """Meta data"""

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "article"],
                name="unique_reaction",
            )
        ]

    def __str__(self) -> str:
        return f"{self.owner}-{self.emoji} -> {self.article}"
