from sklearn.metrics.pairwise import cosine_similarity

from model.age_filter import filter_by_age


def hybrid_safety_filter(df, tfidf_matrix, movie_title, age):

    # =====================================
    # Cosine Similarity
    # =====================================

    similarity_matrix = cosine_similarity(
        tfidf_matrix,
        tfidf_matrix
    )

    # =====================================
    # Cari index film
    # =====================================

    idx = df[df["title"] == movie_title].index

    if len(idx) == 0:
        raise ValueError(f"Film '{movie_title}' tidak ditemukan.")

    idx = idx[0]

    similarity_score = similarity_matrix[idx]

    df = df.copy()

    df["similarity_score"] = similarity_score

    # =====================================
    # Ambil 100 Film Paling Mirip
    # =====================================

    df_top100 = (
        df
        .sort_values(
            by="similarity_score",
            ascending=False
        )
        .head(100)
        .copy()
    )

    # =====================================
    # Age Filter
    # =====================================

    df_age = filter_by_age(
        df_top100,
        age
    )

    jumlah_age = len(df_age)

    # =====================================
    # Safety Filter
    # =====================================

    df_safe = df_age[
        df_age["content_warning"] == False
    ].copy()

    df_safe["imdb_rating"] = df_safe["imdb_rating"].fillna(6.4)

    jumlah_safe = len(df_safe)

    return df_safe, jumlah_age, jumlah_safe