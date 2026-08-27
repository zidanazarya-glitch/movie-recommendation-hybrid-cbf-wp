import streamlit as st

from model.load_data import load_data
from model.recommendation import recommend

# =====================================================
# Header
# =====================================================

st.title("🎬 Sistem Rekomendasi Film")

st.markdown("### 👶 Data Pengguna")

umur = st.number_input(
    "Masukkan Umur Anak",
    min_value=1,
    max_value=17,
    value=10,
    step=1
)

st.divider()

# =====================================================
# Load Dataset
# =====================================================

df = load_data()

movie_list = sorted(df["title"].tolist())

movie = st.selectbox(
    "🎥 Pilih Film yang Disukai",
    movie_list
)

# =====================================================
# Tombol Rekomendasi
# =====================================================

if st.button("🔍 Cari Rekomendasi", use_container_width=True):

    result, jumlah_age, jumlah_safe = recommend(
        movie,
        umur
    )

    if result is None or result.empty:
        st.error("Tidak ditemukan rekomendasi yang sesuai dengan usia pengguna.")
        st.stop()

    # =====================================================
    # Copy Data
    # =====================================================

    result = result.copy()

    # =====================================================
    # Keterangan Age Rating
    # =====================================================

    rating_info = {
        "G": "Semua umur.",
        "PG": "Disarankan didampingi orang tua.",
        "PG-13": "Disarankan untuk usia 13 tahun ke atas.",
        "R": "Di bawah 17 tahun harus didampingi orang tua.",
        "NC-17": "Khusus usia 17 tahun ke atas.",
        "TV-Y": "Program untuk semua anak.",
        "TV-Y7": "Cocok untuk anak usia 7 tahun ke atas.",
        "TV-G": "Program TV untuk semua umur.",
        "TV-PG": "Program TV dengan bimbingan orang tua.",
        "TV-14": "Program TV untuk usia 14 tahun ke atas.",
        "TV-MA": "Program TV khusus dewasa."
    }

    result["Keterangan Rating"] = result["rating"].map(rating_info)

    # =====================================================
    # Content Warning
    # =====================================================

    result["Content Warning"] = result["content_warning"].map({
        False: "Tidak Ada",
        True: "Ada"
    })

    # =====================================================
    # Status Keamanan
    # =====================================================

    result["Status Keamanan"] = result["content_warning"].apply(
        lambda x: "❌ Tidak Aman" if x else "✅ Aman untuk Anak"
    )

    # =====================================================
    # Keterangan
    # =====================================================

    result["Keterangan"] = result["content_warning"].apply(
        lambda x:
        "Film mengandung konten sensitif sehingga tidak direkomendasikan untuk anak."
        if x
        else
        "Film telah lolos Age Rating Filter dan Safety Filter."
    )

    # =====================================================
    # Ranking
    # =====================================================

    result.reset_index(drop=True, inplace=True)
    result.index += 1
    result.index.name = "Ranking"

    # =====================================================
    # Informasi
    # =====================================================

    st.success(
        f"Rekomendasi berhasil dibuat untuk anak usia **{umur} tahun**."
    )

    st.info(
        """
        **Tahapan sistem rekomendasi:**

        1. Content-Based Filtering (TF-IDF + Cosine Similarity)
        2. Age Rating Filter berdasarkan usia pengguna
        3. Safety Filter menggunakan atribut **content_warning**
        4. Perangkingan menggunakan metode **Weighted Product**
        """
    )

    # =====================================================
    # Statistik
    # =====================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🎞 Film Setelah Age Filter",
        jumlah_age
    )

    col2.metric(
        "🛡 Film Lolos Safety Filter",
        jumlah_safe
    )

    col3.metric(
        "⭐ Top Rekomendasi",
        len(result)
    )

    st.divider()

    # =====================================================
    # Hasil
    # =====================================================

    st.subheader("📋 Top 10 Rekomendasi Film")

    st.dataframe(
        result[
            [
                "title",
                "rating",
                "Keterangan Rating",
                "Content Warning",
                "similarity_score",
                "imdb_rating",
                "Vektor_V",
                "Status Keamanan",
                "Keterangan"
            ]
        ],
        use_container_width=True
    )

    st.caption(
        "Keterangan: Age Rating digunakan untuk menyesuaikan rekomendasi dengan usia pengguna, sedangkan Content Warning digunakan sebagai Safety Filter untuk memastikan film yang direkomendasikan aman ditonton anak."
    )