"""
Category model

Fields:
- name: Category name
- description: str
- updated_at: datetime
- created_at: datetime

Methods:
- article_count: Number of articles of a category
"""

from django.db import models


# Create your models here.
class Category(models.Model):
    """Article Categories"""

    name = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        help_text="Category Name",
    )
    description = models.CharField(
        max_length=256,
        db_index=True,
        help_text="Category Description",
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
        """Number of articles of a category"""

        return self.articles.count()

    def __str__(self) -> str:
        return self.name
