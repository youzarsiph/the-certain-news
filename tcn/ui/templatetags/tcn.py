"""TCN Template tags"""

from django import template
from django.urls import reverse_lazy
from wagtail.models import Site

from tcn.apps.categories.models import CategoryIndex

register = template.Library()


# Create your tags here.
@register.simple_tag(takes_context=True)
def short_link(context, slug=None):
    """Generates the short link for an article"""

    url = reverse_lazy("tcn:redirect", args=[slug if slug else "home"])

    return context["request"].build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Get site root"""

    try:
        site = Site.find_for_request(context["request"])

    except KeyError:
        site = Site.objects.filter(is_default_site=True).first()

    return site.root_page.specific.localized


@register.simple_tag()
def get_category_index(home):
    """Get category index from home"""

    return home.get_children().type(CategoryIndex).last()


@register.simple_tag()
def get_menu_items(home):
    """Get category index from home"""

    return home.get_descendants().live().public().in_menu()
