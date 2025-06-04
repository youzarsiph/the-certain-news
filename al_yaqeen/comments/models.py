"""
Comment model

Fields:
- user: Comment owner
- article: Comment article
- content: Comment content
- replies: Comment replies
- updated_at: Last update
- created_at: Date published

Methods:
- reply_count: Number of replies to this comment
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField

from al_yaqeen.mixins.models import DateTimeMixin
from al_yaqeen.users import User


# Create your models here.
class Comment(DateTimeMixin, models.Model):
    """Article Comments"""

    user = models.ForeignKey(
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
        return f"Comment by {self.user} on {self.article}: {self.content[:20]}..."
