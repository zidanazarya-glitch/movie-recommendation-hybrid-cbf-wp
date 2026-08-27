import pandas as pd

def filter_by_age(df, age):

    if age <= 6:

        allowed = [
            "G",
            "TV-Y",
            "TV-G"
        ]

    elif age <= 12:

        allowed = [
            "G",
            "PG",
            "TV-G",
            "TV-Y",
            "TV-Y7",
            "TV-PG"
        ]

    elif age <= 15:

        allowed = [
            "G",
            "PG",
            "PG-13",
            "TV-G",
            "TV-Y",
            "TV-Y7",
            "TV-PG",
            "TV-14"
        ]

    else:

        allowed = [
            "G",
            "PG",
            "PG-13",
            "R",
            "TV-14",
            "TV-PG",
            "TV-MA",
            "TV-G",
            "TV-Y",
            "TV-Y7",
            "NC-17"
        ]

    return df[df["rating"].isin(allowed)].copy()