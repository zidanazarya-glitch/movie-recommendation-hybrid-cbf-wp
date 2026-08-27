import pandas as pd


def load_data(path="dataset/movies.csv"):
    df = pd.read_csv(path)
    return df