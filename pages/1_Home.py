import streamlit as st

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.title("Sistem Rekomendasi Film")

st.markdown("""
### Hybrid Content Based Filtering + Weighted Product

Sistem ini dibuat untuk merekomendasikan film yang **aman ditonton anak di bawah umur**
dengan menggabungkan dua metode:

- Content Based Filtering (TF-IDF + Cosine Similarity)
- Weighted Product

Sistem akan:

1. mencari film yang mirip
2. melakukan Safety Filter menggunakan **content_warning**
3. melakukan perangkingan menggunakan Weighted Product
4. menampilkan Top 10 rekomendasi
""")

st.info("Silakan buka menu **Rekomendasi** pada sidebar.")