"""Load news articles from JSON"""

import json
from secrets import token_urlsafe

from django.core.exceptions import ValidationError
from django.db import transaction
from wagtail.images import get_image_model
from wagtail.models import Locale

from tcn.apps.articles.models import Article
from tcn.apps.categories.models import Category

Image = get_image_model()


def run(src_path: str, language_code: str) -> None:
    """
    Load news articles in specified language to db, with translations

    Args:
        src_path (str): Path to `JSON` data.
        language_code (str): Language code. e.g. 'ar', 'tr'
    """
    try:
        with open(src_path, encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        print(f"{src_path} does not exists")
        return

    locales_cache = {}
    categories_cache = {}

    # Preload base locale (the source tree you’re inserting into)
    try:
        base_locale = Locale.objects.get(language_code=language_code)

    except Locale.DoesNotExist:
        print(f"Locale {language_code} not found")
        return

    def get_locale(code: str) -> Locale:
        if code not in locales_cache:
            locales_cache[code] = Locale.objects.get(language_code=code)
        return locales_cache[code]

    def get_category(slug: str) -> Category:
        key = (slug, base_locale.language_code)
        if key not in categories_cache:
            categories_cache[key] = Category.objects.get(
                slug=slug,
                locale=base_locale,
            )
        return categories_cache[key]

    for item in data:
        # Get a random image
        image = Image.objects.order_by("?").first()

        try:
            with transaction.atomic():
                category = get_category(item["category"])

                # Avoid duplicates in base locale
                existing = (
                    category.get_children()
                    .type(Article)
                    .filter(slug=item["slug"])
                    .first()
                )
                if existing:
                    article = existing.specific
                else:
                    article = Article(
                        slug=item["slug"],
                        title=item["title"],
                        country=item["country"],
                        headline=item["headline"],
                        is_breaking=item["is_breaking"],
                        image=image,
                        locale=base_locale,
                        content=[
                            {
                                "type": "paragraph",
                                "id": token_urlsafe(10),
                                "value": item["content"],
                            }
                        ],
                    )
                    category.add_child(instance=article)
                    # Create a revision for the source page; publish if needed
                    article.save_revision().publish()

                # Create or update translations
                for trans in item.get("translations", []):
                    try:
                        target_locale = get_locale(trans["locale"])
                    except Locale.DoesNotExist:
                        continue

                    if target_locale == base_locale:
                        # Skip if it's the same locale as base
                        continue

                    # Check if translation already exists
                    existing_trans = (
                        article.get_translations().filter(locale=target_locale).first()
                    )
                    if existing_trans:
                        localized_article = existing_trans.specific
                    else:
                        localized_article = article.copy_for_translation(
                            target_locale,
                            copy_parents=True,
                        )

                    # Update localized fields
                    localized_article.title = trans["title"]
                    localized_article.headline = trans["headline"]
                    localized_article.content = [
                        {
                            "type": "paragraph",
                            "id": token_urlsafe(10),
                            "value": trans["content"],
                        }
                    ]

                    # Important: save, create revision, and publish
                    localized_article.save()
                    rev = localized_article.save_revision()
                    rev.publish()
                    localized_article.refresh_from_db()

        except (Category.DoesNotExist, ValidationError):
            continue
