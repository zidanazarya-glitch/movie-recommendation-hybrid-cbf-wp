from model.load_data import load_data
from model.feature_engineering import feature_engineering
from model.safety_filter import hybrid_safety_filter
from model.weighted_product import weighted_product

df = load_data()

df, tfidf, tfidf_matrix = feature_engineering(df)

film = input("Masukkan Judul Film: ")

df_top100 = hybrid_safety_filter(
    df,
    tfidf_matrix,
    film
)

hasil = weighted_product(df_top100)

print("\n===== TOP 10 FILM =====\n")

print(
    hasil[
        [
            "title",
            "similarity_score",
            "imdb_rating",
            "Vektor_S",
            "Vektor_V"
        ]
    ].head(10)
)