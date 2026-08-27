import streamlit as st
import plotly.express as px

from model.eda import (
    dataset_info,
    rating_distribution,
    content_warning_distribution,
    imdb_distribution,
    top_imdb_movies,
    dataset_summary
)

# =====================================================
# HEADER
# =====================================================

st.title("📊 Visualisasi Dataset Film")

st.markdown(
    """
    Halaman ini menampilkan analisis dataset yang digunakan
    pada Sistem Rekomendasi Film Hybrid
    (Content-Based Filtering + Weighted Product).
    """
)

st.divider()

# =====================================================
# DATASET INFO
# =====================================================

info = dataset_info()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "🎬 Jumlah Film",
    info["jumlah_film"]
)

col2.metric(
    "👶 Kategori Rating",
    info["jumlah_rating"]
)

col3.metric(
    "⭐ IMDb Rata-rata",
    info["rata_imdb"]
)

col4.metric(
    "🟢 Film Aman",
    info["film_aman"]
)

col5.metric(
    "🔴 Film Tidak Aman",
    info["film_tidak_aman"]
)

st.divider()

# =====================================================
# DISTRIBUSI AGE RATING
# =====================================================

st.subheader("📌 Distribusi Age Rating")

rating = rating_distribution()

fig = px.bar(
    x=rating.index,
    y=rating.values,
    labels={
        "x": "Age Rating",
        "y": "Jumlah Film"
    },
    text=rating.values
)

fig.update_layout(
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# CONTENT WARNING
# =====================================================

st.subheader("🛡 Distribusi Content Warning")

warning = content_warning_distribution()

fig = px.pie(
    values=warning.values,
    names=warning.index,
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# DISTRIBUSI IMDb
# =====================================================

st.subheader("⭐ Distribusi IMDb Rating")

fig = px.histogram(
    imdb_distribution(),
    nbins=20,
    labels={
        "value": "IMDb Rating"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP 10 IMDb
# =====================================================

st.subheader("🏆 Top 10 Film Berdasarkan IMDb")

top10 = top_imdb_movies()

fig = px.bar(
    top10,
    x="imdb_rating",
    y="title",
    orientation="h",
    text="imdb_rating"
)

fig.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# RINGKASAN DATASET
# =====================================================

st.subheader("📄 Ringkasan Dataset")

st.dataframe(
    dataset_summary(),
    use_container_width=True
)

# =====================================================
# ALUR SISTEM
# =====================================================

st.subheader("🔄 Alur Sistem Rekomendasi")

st.info(
    """
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

Safety Filter (content_warning)

⬇

Weighted Product

⬇

Top 10 Rekomendasi
"""
)