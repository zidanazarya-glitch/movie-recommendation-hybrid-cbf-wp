from model.load_data import load_data

df = load_data()

print(sorted(df["rating"].dropna().unique()))