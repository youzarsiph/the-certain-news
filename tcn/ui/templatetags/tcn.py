"""TCN Template tags"""

from typing import Any, Dict

from django import template
from wagtail.models import Site

from tcn.apps.categories.models import CategoryIndex

register = template.Library()


# Create your tags here.
@register.simple_tag(takes_context=True)
def get_site_root(context: Dict[str, Any]):
    """Get site root"""

    request = context.get("request", None)

    if request:
        return Site.find_for_request(request).root_page.specific.localized

    return (
        Site.objects.filter(is_default_site=True).first().root_page.specific.localized
    )


@register.simple_tag()
def get_category_index(home):
    """Get category index from home"""

    return home.get_children().type(CategoryIndex).last()


@register.simple_tag()
def get_menu_items(home):
    """Get category index from home"""

    return home.get_descendants().live().public().in_menu()[:5]
