"""Custom blocks StreamField"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock


# Create your blocks here.
class TextBlock(blocks.StreamBlock):
    """Custom StreamBlock for Text content"""

    quote = blocks.BlockQuoteBlock(verbose_name=_("quote"), help_text=_("Quote"))
    paragraph = blocks.RichTextBlock(
        verbose_name=_("paragraph"),
        help_text=_("Rich Text"),
    )


class MediaBlock(TextBlock):
    """Custom StreamBlock for Text and Media content"""

    video = EmbedBlock(verbose_name=_("video"), help_text=_("Video"))
    image = ImageBlock(verbose_name=_("image"), help_text=_("Image"))
    document = DocumentChooserBlock(verbose_name=_("document"), help_text=_("Document"))
