from model.recommendation import recommend

movie = "Dragon Legend"
umur = 10

result, jumlah_age, jumlah_safe = recommend(
    movie,
    umur
)

print("=" * 60)
print("HASIL PENGUJIAN")
print("=" * 60)

print(f"Film Acuan              : {movie}")
print(f"Umur                    : {umur}")
print(f"Setelah Age Filter      : {jumlah_age}")
print(f"Setelah Safety Filter   : {jumlah_safe}")
print(f"Top Recommendation      : {len(result)}")

print("=" * 60)

print(
    result[
        [
            "title",
            "rating",
            "content_warning",
            "similarity_score",
            "imdb_rating",
            "Vektor_V"
        ]
    ]
)