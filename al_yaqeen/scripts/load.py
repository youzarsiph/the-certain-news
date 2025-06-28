"""Import categories data"""

import json
import os
import sys

from al_yaqeen.categories.serializers import CategorySerializer


def run(path: str = "categories.json") -> None:
    """Import categories data"""

    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        sys.exit(1)
        return

    with open("categories.json", encoding="utf-8") as o:
        data = json.load(o)
        serializer = CategorySerializer(data, many=True)

        if not serializer.is_valid():
            print("Invalid data")
            sys.exit(1)
            return

        serializer.save()

    print("Import complete")
