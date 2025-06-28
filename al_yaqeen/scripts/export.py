"""Export categories data"""

import json
import sys

from al_yaqeen.categories.models import Category
from al_yaqeen.categories.serializers import CategorySerializer


def run() -> None:
    """Export categories data"""

    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)

    with open("categories.json", "w", encoding="utf-8") as o:
        json.dump(serializer.data, o, indent=2, ensure_ascii=False)

    print("Export complete")
    sys.exit(0)
