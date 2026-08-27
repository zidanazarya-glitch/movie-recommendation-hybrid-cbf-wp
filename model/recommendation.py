from model.load_data import load_data
from model.feature_engineering import feature_engineering
from model.safety_filter import hybrid_safety_filter
from model.weighted_product import weighted_product


def recommend(movie_title, age):

    # ==========================
    # Load Dataset
    # ==========================

    df = load_data()

    # ==========================
    # Feature Engineering
    # ==========================

    df, tfidf, tfidf_matrix = feature_engineering(df)

    # ==========================
    # Similarity
    # ==========================

    df_safe, jumlah_age, jumlah_safe = hybrid_safety_filter(
        df,
        tfidf_matrix,
        movie_title,
        age
    )

    if df_safe.empty:
        return None, 0, 0

    # ==========================
    # Weighted Product
    # ==========================

    ranking = weighted_product(df_safe)

    top10 = ranking.head(10).copy()

    return top10, jumlah_age, jumlah_safe