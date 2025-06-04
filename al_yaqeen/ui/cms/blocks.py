"""Custom blocks StreamField"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


# Create your blocks here.
class TextContentBlock(blocks.StreamBlock):
    """Custom StreamBlock for Text content"""

    heading = blocks.CharBlock(form_classname="title", help_text=_("Heading"))
    paragraph = blocks.RichTextBlock(help_text=_("Paragraph"))


class CommonContentBlock(TextContentBlock):
    """Custom StreamBlock for Text and Media content"""

    image = ImageChooserBlock(help_text=_("Image"))
    document = DocumentChooserBlock(help_text=_("Document"))
