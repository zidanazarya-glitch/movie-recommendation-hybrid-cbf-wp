import streamlit as st
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from model.load_data import load_data
from model.feature_engineering import feature_engineering
from model.age_filter import filter_by_age
from model.weighted_product import weighted_product

st.title("🧮 Proses Perhitungan Sistem")

st.markdown("""
Halaman ini menunjukkan proses perhitungan
Hybrid Recommendation System mulai dari
Content-Based Filtering hingga Weighted Product.
""")

st.divider()

df = load_data()

umur = st.slider(
    "Umur Pengguna",
    1,
    17,
    10
)

movie = st.selectbox(
    "Film Acuan",
    sorted(df["title"])
)

st.header("1️⃣ Feature Engineering")

df, tfidf, tfidf_matrix = feature_engineering(df)

st.success("Feature Engineering berhasil dilakukan.")

st.write("Ukuran TF-IDF Matrix")

st.write(tfidf_matrix.shape)

st.header("2️⃣ Cosine Similarity")

similarity_matrix = cosine_similarity(
    tfidf_matrix,
    tfidf_matrix
)

idx = df[df["title"] == movie].index[0]

score = similarity_matrix[idx]

df_similarity = df.copy()

df_similarity["similarity_score"] = score

df_similarity = df_similarity.sort_values(
    "similarity_score",
    ascending=False
)

st.dataframe(

    df_similarity[

        [

            "title",

            "similarity_score"

        ]

    ].head(15),

    use_container_width=True

)

st.header("3️⃣ Age Rating Filter")

df_age = filter_by_age(
    df_similarity,
    umur
)

st.metric(

    "Jumlah Film Setelah Age Filter",

    len(df_age)

)

st.dataframe(

    df_age[

        [

            "title",

            "rating",

            "similarity_score"

        ]

    ].head(15),

    use_container_width=True

)

st.header("4️⃣ Safety Filter")

df_safe = df_age[
    df_age["content_warning"] == False
]

st.metric(

    "Jumlah Film Aman",

    len(df_safe)

)

st.dataframe(

    df_safe[

        [

            "title",

            "rating",

            "content_warning",

            "similarity_score"

        ]

    ].head(15),

    use_container_width=True

)

st.header("5️⃣ Weighted Product")

ranking = weighted_product(
    df_safe
)

st.dataframe(

    ranking[

        [

            "title",

            "similarity_score",

            "imdb_rating",

            "Vektor_V"

        ]

    ].head(10),

    use_container_width=True

)

st.header("🏆 Top Recommendation")

top10 = ranking.head(10)

top10 = top10.copy()

top10.index += 1

st.dataframe(

    top10[

        [

            "title",

            "rating",

            "content_warning",

            "similarity_score",

            "imdb_rating",

            "Vektor_V"

        ]

    ],

    use_container_width=True

)

st.header("🔄 Alur Perhitungan")

st.info("""

Dataset Film

⬇

Feature Engineering

⬇

TF-IDF

⬇

Cosine Similarity

⬇

Age Rating Filter

⬇

Safety Filter

⬇

Weighted Product

⬇

Top 10 Recommendation

""")

st.header("📄 Kesimpulan Perhitungan")

film_terbaik = top10.iloc[0]["title"]

nilai = round(
    top10.iloc[0]["Vektor_V"],
    4
)

st.success(f"""

Film yang dipilih pengguna adalah **{movie}**.

Age Rating Filter berhasil menyaring film
berdasarkan usia **{umur} tahun**.

Safety Filter berhasil menghilangkan film
yang memiliki content_warning=True.

Metode Weighted Product menghasilkan
peringkat akhir berdasarkan nilai preferensi.

Film dengan nilai tertinggi adalah

**{film_terbaik}**

dengan nilai Vektor V sebesar

**{nilai}**

""")

