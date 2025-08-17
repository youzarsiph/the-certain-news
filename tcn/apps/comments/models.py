"""Comment model"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField

from tcn.apps.mixins import DateTimeMixin

# Create your models here.
User = get_user_model()


class Comment(DateTimeMixin, models.Model):
    """Article Comments"""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_("Comment Owner"),
    )
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        help_text=_("Commented Article"),
    )
    content = RichTextField(
        db_index=True,
        help_text=_("Comment Content"),
    )
    replies = models.ManyToManyField(
        "self",
        symmetrical=False,
        help_text=_("Comment Replies"),
    )

    @property
    def reply_count(self) -> int:
        """Number of replies to this comment"""

        return self.replies.count()

    def __str__(self) -> str:
        return f"{self.owner}-{self.article}"
