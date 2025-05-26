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

from al_yaqeen.users import User


# Create your models here.
class Comment(models.Model):
    """Article Comments"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Comment Owner",
    )
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        help_text="Commented Article",
    )
    content = models.TextField(
        db_index=True,
        help_text="Content",
    )
    replies = models.ManyToManyField(
        "self",
        symmetrical=False,
        help_text="Comment Replies",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date published",
    )

    @property
    def reply_count(self) -> int:
        """Number of replies to this comment"""

        return self.replies.count()

    def __str__(self) -> str:
        return f"Comment by {self.user} on {self.article}: {self.content[:20]}..."
