from model.load_data import load_data
from model.feature_engineering import feature_engineering

df = load_data()

df, tfidf, tfidf_matrix = feature_engineering(df)

print(df.head())

print(tfidf_matrix.shape)