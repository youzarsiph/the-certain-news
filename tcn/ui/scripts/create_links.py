"""Create links for articles with no links"""

from tcn.apps.articles.models import Article
from tcn.apps.links.models import Link


def run():
    """Create links"""

    Link.objects.bulk_create(
        [Link(article=article) for article in Article.objects.filter(link=None)]
    )
