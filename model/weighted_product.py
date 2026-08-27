import pandas as pd


def weighted_product(df_top100):
    """
    Menghitung ranking menggunakan metode Weighted Product.

    Kriteria:
    1. Similarity Score (Benefit)
    2. IMDb Rating (Benefit)

    Bobot:
    Similarity = 0.6
    IMDb       = 0.4
    """

    df = df_top100.copy()

    # =====================================================
    # Bobot Kriteria
    # =====================================================

    w_similarity = 0.6
    w_imdb = 0.4

    # =====================================================
    # Mengatasi Missing Value IMDb
    # =====================================================

    df["imdb_rating"] = df["imdb_rating"].fillna(0)

    # =====================================================
    # Normalisasi IMDb
    # =====================================================

    max_imdb = df["imdb_rating"].max()

    if max_imdb > 0:
        df["imdb_norm"] = df["imdb_rating"] / max_imdb
    else:
        df["imdb_norm"] = 0

    # =====================================================
    # Pangkat Weighted Product
    # =====================================================

    df["similarity_pow"] = (
        df["similarity_score"] ** w_similarity
    )

    df["imdb_pow"] = (
        df["imdb_norm"] ** w_imdb
    )

    # =====================================================
    # Vektor S
    # =====================================================

    df["Vektor_S"] = (

        df["similarity_pow"]

        *

        df["imdb_pow"]

    )

    # =====================================================
    # Total Vektor S
    # =====================================================

    total_s = df["Vektor_S"].sum()

    # =====================================================
    # Vektor V
    # =====================================================

    if total_s > 0:

        df["Vektor_V"] = (

            df["Vektor_S"]

            /

            total_s

        )

    else:

        df["Vektor_V"] = 0

    # =====================================================
    # Ranking
    # =====================================================

    df = df.sort_values(

        by="Vektor_V",

        ascending=False

    ).reset_index(drop=True)

    # =====================================================
    # Ranking Akhir
    # =====================================================

    df.index += 1
    df.index.name = "Ranking"

    return df