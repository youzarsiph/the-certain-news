"""
Tag model

Fields:
- name: Tag name
- color: Tag color
- description: Tag description
- updated_at: Last update
- created_at: Date created
"""

from django.db import models


# Create your models here.
class Tag(models.Model):
    """Article Tags"""

    name = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        help_text="Tag Name",
    )
    color = models.CharField(
        max_length=8,
        unique=True,
        db_index=True,
        help_text="Tag color",
    )
    description = models.CharField(
        max_length=256,
        db_index=True,
        help_text="Tag Description",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date created",
    )

    @property
    def article_count(self) -> int:
        """Number of articles of a tag"""

        return self.articles.count()

    def __str__(self) -> str:
        return self.name
