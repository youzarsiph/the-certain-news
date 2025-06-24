"""
Reaction model

Fields:
- user: Reaction owner
- article: Article reacted to
- emoji: Reaction emoji
- updated_at: Last update
- created_at: Date reacted
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from al_yaqeen.mixins.models import DateTimeMixin
from al_yaqeen.reactions import REACTIONS
from al_yaqeen.users import User


# Create your models here.
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
        help_text=_("Reaction"),
        choices=REACTIONS,
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
        return f"{self.owner}---{self.emoji}-> {self.article}"
