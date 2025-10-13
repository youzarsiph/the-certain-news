"""Custom blocks StreamField"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail_blocks import blocks as w_blocks


# Create your blocks here.
class TextBlock(blocks.StreamBlock):
    """Custom StreamBlock for Text content"""

    alert = w_blocks.AlertBlock(
        verbose_name=_("alert"),
        help_text=_("Alert"),
    )
    accordion = w_blocks.AccordionBlock(
        verbose_name=_("accordion"),
        help_text=_("Accordion"),
    )
    quote = blocks.BlockQuoteBlock(
        verbose_name=_("quote"),
        help_text=_("Quote"),
    )
    paragraph = blocks.RichTextBlock(
        verbose_name=_("paragraph"),
        help_text=_("Rich Text"),
    )
    timeline = w_blocks.TimelineBlock(
        verbose_name=_("timeline"),
        help_text=_("Timeline"),
    )
    steps = w_blocks.StepsBlock(
        verbose_name=_("steps"),
        help_text=_("Steps"),
    )
    list = w_blocks.ListBlock(
        verbose_name=_("list"),
        help_text=_("List"),
    )
    tabs = w_blocks.TabsBlock(
        verbose_name=_("tabs"),
        help_text=_("Tabs"),
    )


class MediaBlock(TextBlock):
    """Custom StreamBlock for Text and Media content"""

    video = EmbedBlock(
        verbose_name=_("video"),
        help_text=_("Video"),
    )
    image = w_blocks.ImageBlock(
        verbose_name=_("image"),
        help_text=_("Image"),
    )
    carousel = w_blocks.CarouselBlock(
        verbose_name=_("carousel"),
        help_text=_("Carousel"),
    )
    diff = w_blocks.DiffBlock(
        verbose_name=_("diff"),
        help_text=_("Diff (To compare 2 images)"),
    )
    document = DocumentChooserBlock(
        verbose_name=_("document"),
        help_text=_("Document"),
    )
    hover_gallery = w_blocks.HoverGalleryBlock(
        verbose_name=_("hover gallery"),
        help_text=_("Hover gallery"),
    )
    browser_mockup = w_blocks.BrowserMockupBlock(
        verbose_name=_("browser mockup"),
        help_text=_("Browser mockup"),
    )
    phone_mockup = w_blocks.PhoneMockupBlock(
        verbose_name=_("phone mockup"),
        help_text=_("Phone mockup"),
    )


class ExternalLinkBlock(blocks.StructBlock):
    """External links"""

    icon = blocks.CharBlock(
        required=False,
        verbose_name=_("icon"),
        help_text=_("Link icon (Lucide icons)"),
    )
    url = blocks.URLBlock(
        required=False,
        verbose_name=_("url"),
        help_text=_("URL"),
    )
    label = blocks.CharBlock(
        required=True,
        verbose_name=_("label"),
        help_text=_("Link label"),
    )


class InternalLinkBlock(blocks.StructBlock):
    """Internal links"""

    icon = blocks.CharBlock(
        required=False,
        verbose_name=_("icon"),
        help_text=_("Link icon (Lucide icons)"),
    )
    page = blocks.PageChooserBlock(
        required=False,
        verbose_name=_("page"),
        help_text=_("Link to a page"),
    )
    label = blocks.CharBlock(
        required=True,
        verbose_name=_("label"),
        help_text=_("Link label"),
    )


class LinkBlock(ExternalLinkBlock, InternalLinkBlock):
    """Link blocks"""

    class Meta:
        """Meta data"""

        icon = "link"


class SectionBlock(blocks.StructBlock):
    """Menu sections"""

    title = blocks.CharBlock(
        max_length=255,
        verbose_name=_("title"),
        help_text=_("Section title"),
    )
    links = blocks.ListBlock(
        LinkBlock(),
        label=_("links"),
        help_text=_("List of links"),
    )

    class Meta:
        """Meta data"""

        icon = "table"


class FooterBlock(blocks.StructBlock):
    """Footer block"""

    title = blocks.CharBlock(
        required=True,
        label=_("Title"),
        help_text=_("Same as Home page title"),
    )
    headline = blocks.CharBlock(
        required=True,
        label=_("Headline"),
        help_text=_("Headline"),
    )
    social = blocks.ListBlock(
        ExternalLinkBlock(),
        label=_("Social media links"),
        help_text=_("List of social media links"),
    )
    sections = blocks.ListBlock(
        SectionBlock(),
        label=_("Navigation sections"),
        help_text=_("List of footer nav sections"),
    )

    class Meta:
        """Meta data"""

        icon = "minus"
        template = "tcn/blocks/footer.html"
        block_counts = {
            "social": {"min_num": 1, "max_num": 1},
            "sections": {"min_num": 1, "max_num": 1},
        }


class FooterStreamBlock(blocks.StreamBlock):
    """Footer stream block"""

    footer = FooterBlock()
