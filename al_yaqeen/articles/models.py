"""
Article model

Fields:
- user: Article owner
- category: Article category
- photo: Article photo
- title: Article title
- headline: Article headline
- content: Article content
- is_pinned: Designates if the Article is pinned
- comments: Article comments
- reactions: Article reactions
- recommendations: Similar articles
- stargazers: Article stargazers
- reports: Article reports
- tags: Article tags
- updated_at: Last update
- created_at: Date published

Methods:
- comment_count: Number of comments of an article
- reaction_count: Number of reactions of an article
- star_count: Number of stargazers of an article
- report_count: Number of reports of an article
- recommendation_count: Number of recommendations of an article
- tag_count: Number of tags of an article
"""

from django.db import models

from al_yaqeen.users import User


# Create your models here.
class Article(models.Model):
    """Articles"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        help_text="Article owner",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.CASCADE,
        related_name="articles",
        help_text="Article category",
    )
    photo = models.ImageField(
        null=True,
        blank=True,
        help_text="Article Photo",
        upload_to="al_yaqeen/images/articles/",
    )
    title = models.CharField(
        max_length=64,
        db_index=True,
        help_text="Article title",
    )
    headline = models.CharField(
        max_length=256,
        db_index=True,
        help_text="Article headline",
    )
    content = models.TextField(
        db_index=True,
        help_text="Article content",
    )
    is_pinned = models.BooleanField(
        default=False,
        help_text="Designates if the Article is pinned",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        blank=True,
        related_name="articles",
        help_text="Article tags",
    )
    comments = models.ManyToManyField(
        User,
        related_name="comments",
        through="comments.Comment",
        help_text="Article comments",
    )
    reactions = models.ManyToManyField(
        User,
        related_name="reactions",
        through="reactions.Reaction",
        help_text="Article reactions",
    )
    recommendations = models.ManyToManyField(
        "self",
        symmetrical=True,
        help_text="Similar articles",
    )
    stargazers = models.ManyToManyField(
        User,
        related_name="stargazers",
        help_text="Article stargazers",
    )
    reports = models.ManyToManyField(
        User,
        related_name="reports",
        through="reports.Report",
        help_text="Article reports",
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
    def comment_count(self) -> int:
        """Number of comments of an article"""

        return self.comments.count()

    @property
    def reaction_count(self) -> int:
        """Number of reactions of an article"""

        return self.reactions.count()

    @property
    def report_count(self) -> int:
        """Number of reports of an article"""

        return self.reports.count()

    @property
    def tag_count(self) -> int:
        """Number of tags of an article"""

        return self.tags.count()

    @property
    def stars(self) -> int:
        """Number of stars of an article"""

        return self.stargazers.count()

    def __str__(self) -> str:
        return self.title
