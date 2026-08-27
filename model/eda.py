import pandas as pd

from model.load_data import load_data


# =====================================================
# Load Dataset
# =====================================================

df = load_data()


# =====================================================
# Informasi Dataset
# =====================================================

def dataset_info():

    info = {

        "jumlah_film": len(df),

        "jumlah_rating": df["rating"].nunique(),

        "rata_imdb": round(
            df["imdb_rating"].mean(),
            2
        ),

        "film_aman": len(
            df[df["content_warning"] == False]
        ),

        "film_tidak_aman": len(
            df[df["content_warning"] == True]
        )

    }

    return info


# =====================================================
# Distribusi Age Rating
# =====================================================

def rating_distribution():

    rating = (

        df["rating"]

        .value_counts()

        .sort_index()

    )

    return rating


# =====================================================
# Distribusi Content Warning
# =====================================================

def content_warning_distribution():

    warning = (

        df["content_warning"]

        .replace(

            {

                False: "Tidak Ada",

                True: "Ada"

            }

        )

        .value_counts()

    )

    return warning


# =====================================================
# Distribusi IMDb
# =====================================================

def imdb_distribution():

    return df["imdb_rating"].dropna()


# =====================================================
# Top 10 IMDb
# =====================================================

def top_imdb_movies():

    top10 = (

        df

        .sort_values(

            by="imdb_rating",

            ascending=False

        )

        .head(10)

    )

    return top10[
        [

            "title",

            "imdb_rating",

            "rating"

        ]

    ]


# =====================================================
# Statistik Rating
# =====================================================

def rating_statistics():

    return (

        df

        .groupby("rating")

        ["imdb_rating"]

        .mean()

        .round(2)

    )


# =====================================================
# Statistik Content Warning
# =====================================================

def warning_statistics():

    return (

        df

        .groupby("content_warning")

        .size()

    )


# =====================================================
# Ringkasan Dataset
# =====================================================

def dataset_summary():

    summary = df.describe(

        include="all"

    )

    return summary