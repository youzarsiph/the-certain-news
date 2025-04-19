"""Script for computing recommendations using Content Based Filtering algorithm"""

import polars as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from al_yaqeen.articles.models import Article


def run() -> None:
    """Compute article recommendations"""

    print("Computing recommendations")

    # Article data
    df = pd.DataFrame(
        [
            {
                "id": article.pk,
                "title": article.title,
                "headline": article.headline,
                "content": article.content,
                "created_at": article.created_at,
                "updated_at": article.updated_at,
            }
            for article in Article.objects.all()
        ]
    )

    # Compute similar articles
    similar_articles = cosine_similarity(
        TfidfVectorizer(stop_words="english").fit_transform(
            [
                f"""{a['title']}
                Date published: {a['created_at']}, Last update: {a['updated_at']}
                {a['headline']}
                {a['content']}"""
                for a in df.to_dicts()
            ]
        )
    )

    # Add recommendations to data-frame
    # df["recommendations"] = [
    #     df["id"].loc[x.argsort()[-5:-1]].tolist() for x in similar_articles
    # ]

    df.with_columns(recommendations=pd.col("id"))

    df["recommendations"] = [
        df["id"].fil[x.argsort()[-5:-1]].to_list() for x in similar_articles
    ]

    # Add recommendations to database
    for a in df[["id", "recommendations"]].to_dicts():
        # Get article
        article = Article.objects.get(id=a["id"])

        # Clear recommendations
        article.recommendations.clear()

        # Add recommended articles
        article.recommendations.add(*a["recommendations"])

    print("All Done")
