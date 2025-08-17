"""Custom API fields"""

from rest_framework.fields import CharField
from wagtail.rich_text import expand_db_html


class RichTextField(CharField):
    """Rich text field"""

    def to_representation(self, instance):
        """Transform the outgoing native value into primitive data (HTML)."""

        return expand_db_html(super().to_representation(instance))
