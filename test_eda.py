from model.eda import (
    dataset_info,
    rating_distribution,
    content_warning_distribution,
    top_imdb_movies
)

print("=" * 60)
print("INFORMASI DATASET")
print("=" * 60)

print(dataset_info())

print()

print("=" * 60)
print("DISTRIBUSI RATING")
print("=" * 60)

print(rating_distribution())

print()

print("=" * 60)
print("CONTENT WARNING")
print("=" * 60)

print(content_warning_distribution())

print()

print("=" * 60)
print("TOP 10 IMDb")
print("=" * 60)

print(top_imdb_movies())