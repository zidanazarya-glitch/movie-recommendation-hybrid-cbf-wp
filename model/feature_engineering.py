import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def feature_engineering(df):

    df = df.copy()

    df["genre_primary"] = df["genre_primary"].fillna("")
    df["genre_secondary"] = df["genre_secondary"].fillna("")
    df["content_type"] = df["content_type"].fillna("")
    df["language"] = df["language"].fillna("")

    df["metadata"] = (

        df["genre_primary"].astype(str)

        + " "

        + df["genre_secondary"].astype(str)

        + " "

        + df["content_type"].astype(str)

        + " "

        + df["language"].astype(str)

    )

    df["metadata"] = (

        df["metadata"]

        .str.lower()

        .str.replace(",", " ", regex=False)

        .str.replace("-", " ", regex=False)

    )

    tfidf = TfidfVectorizer(stop_words="english")

    tfidf_matrix = tfidf.fit_transform(df["metadata"])

    return df, tfidf, tfidf_matrix