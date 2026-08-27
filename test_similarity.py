from model.load_data import load_data
from model.feature_engineering import feature_engineering
from model.safety_filter import hybrid_safety_filter

df = load_data()

df, tfidf, tfidf_matrix = feature_engineering(df)

film = input("Masukkan Judul Film : ")

hasil = hybrid_safety_filter(
    df,
    tfidf_matrix,
    film
)

print()

print(
    hasil[
        [
            "title",
            "similarity_score",
            "imdb_rating"
        ]
    ].head(10)
)