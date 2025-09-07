"""TCN Template tags"""

from django import template
from django.urls import reverse_lazy
from wagtail.models import Page, Site
from wagtail.templatetags.wagtailcore_tags import pageurl, slugurl

register = template.Library()


# Create your tags here.
@register.simple_tag(takes_context=True)
def short_link(context, slug=None):
    """Generates the short link for an article"""

    url = reverse_lazy("ui:redirect", args=[slug if slug else "home"])

    return context["request"].build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def slug_url(context, slug, language_code):
    """
    Returns the URL for the page that has the given slug.

    First tries to find a page on the current site. If that fails or a request
    is not available in the context, then returns the URL for the first page
    that matches the slug on any site.
    """

    page = None

    try:
        site = Site.find_for_request(context["request"])
        current_site = site

    except KeyError:
        # No site object found - allow the fallback below to take place.
        pass

    else:
        if current_site is not None:
            page = (
                Page.objects.in_site(current_site)
                .filter(slug=slug, locale__language_code=language_code)
                .first()
            )

    # If no page is found, fall back to searching the whole tree.
    if page is None:
        page = Page.objects.filter(
            slug=slug, locale__language_code=language_code
        ).first()

    if page:
        # call pageurl() instead of page.relative_url() here so we get the ``accepts_kwarg`` logic
        return pageurl(context, page, language_code)

    else:
        return slugurl(context, slug)


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Get site root"""

    return Site.find_for_request(context["request"]).root_page
