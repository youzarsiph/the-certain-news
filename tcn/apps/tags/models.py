"""Data Models for tcn.apps.tags"""

from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

# Create your models here.


class ArticleTag(TaggedItemBase):
    """Through model for defining m2m rel between Articles and Tags"""

    content_object = ParentalKey(
        "articles.Article",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class PostTag(TaggedItemBase):
    """Through model for defining m2m rel between Posts and Tags"""

    content_object = ParentalKey(
        "blog.Post",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )
