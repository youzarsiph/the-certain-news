"""Model mixins"""

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your model mixins here.
class DateTimeMixin(models.Model):
    """Provide `created_at` and `updated_at` for a model"""

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("Last update"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Date created"),
    )

    class Meta:
        """Meta data"""

        abstract = True
