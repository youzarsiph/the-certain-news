"""Custom blocks StreamField"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock


# Create your blocks here.
class TextContentBlock(blocks.StreamBlock):
    """Custom StreamBlock for Text content"""

    quote = blocks.BlockQuoteBlock(help_text=_("Quote"))
    paragraph = blocks.RichTextBlock(help_text=_("Paragraph"))
    table = TableBlock(help_text=_("Table"))
    table_typed = TypedTableBlock(
        [
            ("text", blocks.CharBlock()),
            ("numeric", blocks.FloatBlock()),
            ("rich_text", blocks.RichTextBlock()),
            ("image", ImageBlock()),
            (
                "country",
                blocks.ChoiceBlock(
                    choices=[
                        ("be", "Belgium"),
                        ("fr", "France"),
                        ("de", "Germany"),
                        ("nl", "Netherlands"),
                        ("pl", "Poland"),
                        ("uk", "United Kingdom"),
                    ]
                ),
            ),
        ]
    )


class CommonContentBlock(TextContentBlock):
    """Custom StreamBlock for Text and Media content"""

    image = ImageBlock(help_text=_("Image"))
    video = EmbedBlock(help_text=_("Video Embed URL"))
    document = DocumentChooserBlock(help_text=_("Document"))
