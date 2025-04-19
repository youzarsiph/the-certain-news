"""
Report model

Fields:
- user: Report owner
- article: Reported article
- is_approved: Designates if the abuse report is correct
- message: Message that will help us understand and handle the situation
- reason: Report reason
- updated_at: Last update
- created_at: Date published
"""

from django.db import models


from al_yaqeen.reports import REPORT_REASONS
from al_yaqeen.users import User


# Create your models here.
class Report(models.Model):
    """Abuse Reports"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Reporter",
    )
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        help_text="Reported Article",
    )
    is_approved = models.BooleanField(
        default=False,
        help_text="Designates if the abuse report is correct",
    )
    message = models.CharField(
        max_length=256,
        db_index=True,
        help_text="Message that will help us understand and handle the situation",
    )
    reason = models.PositiveSmallIntegerField(
        default=0,
        db_index=True,
        help_text="Report reason",
        choices=REPORT_REASONS,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date published",
    )

    def __str__(self) -> str:
        return f"{self.user} --{REPORT_REASONS[self.reason][1]}-> {self.article}"
