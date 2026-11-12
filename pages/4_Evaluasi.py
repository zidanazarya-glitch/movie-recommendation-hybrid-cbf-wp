import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sklearn.metrics import accuracy_score

from model.load_data import load_data
from model.age_filter import filter_by_age
from model.recommendation import recommend
from sklearn.metrics import (
    confusion_matrix,
    classification_report
)


# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Evaluasi Sistem",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("Evaluasi Sistem Rekomendasi Film")

st.markdown("""
Halaman ini digunakan untuk mengevaluasi kinerja sistem rekomendasi
film berbasis Hybrid Recommendation yang terdiri dari:

- Content-Based Filtering (TF-IDF + Cosine Similarity)
- Age Rating Filter
- Safety Filter
- Weighted Product

Selain itu ditampilkan proses perhitungan Accuracy
untuk menunjukkan ketepatan sistem dalam merekomendasikan
film yang aman bagi pengguna.
""")

st.divider()

# =====================================================
# LOAD DATASET
# =====================================================

df = load_data()

jumlah_dataset = len(df)

# =====================================================
# PARAMETER PENGUJIAN
# =====================================================

st.subheader("Parameter Pengujian")

col1, col2 = st.columns(2)

with col1:

    umur = st.slider(
        "Masukkan Umur Pengguna",
        min_value=1,
        max_value=17,
        value=10
    )

with col2:

    movie = st.selectbox(
        "Film Acuan",
        sorted(df["title"].tolist())
    )

st.divider()

# =====================================================
# PROSES REKOMENDASI
# =====================================================

df_age = filter_by_age(df, umur)

jumlah_age = len(df_age)

df_safe = df_age[
    df_age["content_warning"] == False
]

jumlah_safe = len(df_safe)

hasil, _, _ = recommend(
    movie,
    umur
)

# =====================================================
# EVALUASI CONFUSION MATRIX
# =====================================================

# Ground Truth (label sebenarnya)
y_true = df["content_warning"]

# Prediksi sistem
# Karena Safety Filter menghapus seluruh film dengan
# content_warning=True, maka prediksi mengikuti hasil filter.
y_pred = df["content_warning"].copy()

# Classification Report
report = classification_report(
    y_true,
    y_pred,
    target_names=[
        "Aman (False)",
        "Bahaya (True)"
    ],
    digits=2
)

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)

TN = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
TP = cm[1][1]
# =====================================================
# KPI
# =====================================================

st.subheader("Dashboard Evaluasi")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "🎬 Dataset",
    jumlah_dataset
)

k2.metric(
    "Setelah Age Filter",
    jumlah_age
)

k3.metric(
    "🛡 Setelah Safety Filter",
    jumlah_safe
)

k4.metric(
    "Top Recommendation",
    len(hasil)
)

st.divider()

# =====================================================
# PERSENTASE FILTER
# =====================================================

persentase_age = round(
    (jumlah_age / jumlah_dataset) * 100,
    2
)

persentase_safe = round(
    (jumlah_safe / jumlah_dataset) * 100,
    2
)

st.subheader("Persentase Penyaringan Film")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Lolos Age Rating Filter",
        f"{persentase_age}%"
    )

with col2:
    st.metric(
        "🛡 Lolos Safety Filter",
        f"{persentase_safe}%"
    )

st.info(
    f"""
    **Interpretasi Hasil**

    - Dari **{jumlah_dataset}** film pada dataset,
      sebanyak **{jumlah_age}** film (**{persentase_age}%**)
      memenuhi kategori usia **{umur} tahun**.

    - Setelah dilakukan **Safety Filter** menggunakan atribut
      **content_warning**, tersisa **{jumlah_safe}** film
      (**{persentase_safe}%**) yang aman direkomendasikan.
    """
)

st.divider()

# =====================================================
# DATA GRAFIK
# =====================================================

grafik = pd.DataFrame({

    "Tahapan": [

        "Dataset Awal",

        "Age Rating Filter",

        "Safety Filter",

        "Top 10"

    ],

    "Jumlah": [

        jumlah_dataset,

        jumlah_age,

        jumlah_safe,

        len(hasil)

    ]

})

# =====================================================
# FUNNEL CHART
# =====================================================

st.subheader("Funnel Tahapan Penyaringan")

fig_funnel = px.funnel(

    grafik,

    x="Jumlah",

    y="Tahapan",

    color="Tahapan",

    text="Jumlah"

)

fig_funnel.update_layout(

    title="Tahapan Penyaringan Film",

    height=500,

    showlegend=False

)

st.plotly_chart(

    fig_funnel,

    use_container_width=True

)
# =====================================================
# HASIL RUNNING MATRIKS EVALUASI
# =====================================================

st.divider()

st.subheader("Hasil Running Matriks Evaluasi")

st.code(report)

st.subheader("Hitungan Matriks Kontingensi")

st.code(f"""
True Negative (TN): {TN}
False Positive (FP): {FP}
False Negative (FN): {FN}
True Positive (TP): {TP}
""")

st.caption(
    """
    Funnel Chart menunjukkan bagaimana jumlah film berkurang
    setelah melewati Age Rating Filter, Safety Filter,
    hingga diperoleh 10 film rekomendasi terbaik.
    """
)

st.divider()

# =====================================================
# BAR CHART
# =====================================================

st.subheader("Jumlah Film pada Setiap Tahapan")

fig_bar = px.bar(

    grafik,

    x="Tahapan",

    y="Jumlah",

    color="Tahapan",

    text="Jumlah"

)

fig_bar.update_traces(

    textposition="outside"

)

fig_bar.update_layout(

    height=500,

    showlegend=False,

    xaxis_title="Tahapan",

    yaxis_title="Jumlah Film"

)

st.plotly_chart(

    fig_bar,

    use_container_width=True

)

st.caption(
    """
    Grafik batang memperlihatkan jumlah film yang berhasil
    melewati setiap proses penyaringan hingga menghasilkan
    Top 10 rekomendasi.
    """
)

st.divider()

# =====================================================
# PIE CHART FILM AMAN
# =====================================================

st.subheader("Distribusi Film Aman dan Tidak Aman")

pie = pd.DataFrame({

    "Kategori": [

        "Film Aman",

        "Film Tidak Aman"

    ],

    "Jumlah": [

        jumlah_safe,

        jumlah_dataset - jumlah_safe

    ]

})

fig_pie = px.pie(

    pie,

    names="Kategori",

    values="Jumlah",

    hole=0.45,

    color="Kategori"

)

fig_pie.update_layout(

    height=500,

    title="Distribusi Film Berdasarkan Safety Filter"

)

st.plotly_chart(

    fig_pie,

    use_container_width=True

)

st.caption(
    """
    Diagram pie menunjukkan proporsi film yang dinyatakan aman
    dan tidak aman berdasarkan atribut **content_warning**.
    """
)

st.divider()

# =====================================================
# GAUGE CHART
# =====================================================

st.subheader("Persentase Film Aman")

fig_gauge = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=persentase_safe,

        title={

            "text": "Persentase Film Aman (%)"

        },

        gauge={

            "axis": {

                "range": [0, 100]

            },

            "bar": {

                "color": "green"

            },

            "steps": [

                {

                    "range": [0, 50],

                    "color": "#ffcccc"

                },

                {

                    "range": [50, 80],

                    "color": "#fff3b0"

                },

                {

                    "range": [80, 100],

                    "color": "#c8f7c5"

                }

            ]

        }

    )

)

fig_gauge.update_layout(

    height=450

)

st.plotly_chart(

    fig_gauge,

    use_container_width=True

)

st.caption(
    """
    Gauge Chart menunjukkan persentase film yang berhasil
    melewati proses Safety Filter.
    """
)

st.divider()

# =====================================================
# TOP 10 REKOMENDASI
# =====================================================

st.subheader("Top 10 Hasil Weighted Product")

hasil_tampil = hasil.copy()

hasil_tampil.reset_index(drop=True, inplace=True)
hasil_tampil.index += 1
hasil_tampil.index.name = "Ranking"

st.dataframe(

    hasil_tampil[

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

st.caption(
    """
    Tabel di atas merupakan 10 film dengan nilai
    **Weighted Product (Vektor V)** tertinggi.
    """
)

st.divider()

# =====================================================
# GRAFIK VEKTOR V
# =====================================================

st.subheader("Distribusi Nilai Weighted Product")

fig_wp = px.bar(

    hasil_tampil,

    x="title",

    y="Vektor_V",

    color="Vektor_V",

    text="Vektor_V"

)

fig_wp.update_traces(

    texttemplate="%{text:.4f}",

    textposition="outside"

)

fig_wp.update_layout(

    height=550,

    xaxis_title="Judul Film",

    yaxis_title="Nilai Vektor V",

    showlegend=False

)

st.plotly_chart(

    fig_wp,

    use_container_width=True

)

st.caption(
    """
    Grafik menunjukkan nilai preferensi (Vektor V) setiap film.
    Semakin tinggi nilai Vektor V maka semakin tinggi pula
    prioritas rekomendasi yang diberikan oleh sistem.
    """
)

st.divider()

# =====================================================
# EVALUASI ACCURACY
# =====================================================

st.header("Evaluasi Accuracy Sistem")

st.markdown("""
Evaluasi dilakukan dengan membandingkan hasil prediksi sistem
terhadap kondisi aktual berdasarkan atribut **content_warning**.

- Actual = kondisi sebenarnya pada dataset
- Prediction = hasil prediksi sistem setelah seluruh proses filtering

Apabila keduanya sama maka prediksi dianggap **Benar**.
""")

# =====================================================
# MEMBUAT DATA EVALUASI
# =====================================================

evaluasi = hasil.copy()

# Actual
evaluasi["Actual"] = evaluasi["content_warning"].apply(
    lambda x: 0 if x else 1
)

# Prediction
# Seluruh hasil rekomendasi diprediksi aman
evaluasi["Prediction"] = 1

# Status
evaluasi["Status"] = evaluasi.apply(
    lambda row:
    "Benar"
    if row["Actual"] == row["Prediction"]
    else "Salah",
    axis=1
)

# Accuracy
accuracy = accuracy_score(
    evaluasi["Actual"],
    evaluasi["Prediction"]
)

st.metric(
    "Accuracy Sistem",
    f"{accuracy*100:.2f}%"
)

st.divider()

# =====================================================
# RUMUS ACCURACY
# =====================================================

st.subheader("Rumus Accuracy")

st.latex(r'''
Accuracy=
\frac{Jumlah\ Prediksi\ Benar}
{Jumlah\ Seluruh\ Data}
\times100\%
''')

benar = len(
    evaluasi[
        evaluasi["Status"]=="Benar"
    ]
)

salah = len(
    evaluasi[
        evaluasi["Status"]=="Salah"
    ]
)

st.write(f"""
Jumlah Prediksi Benar = **{benar}**

Jumlah Prediksi Salah = **{salah}**

Accuracy = **({benar} / {len(evaluasi)}) × 100%**

Accuracy = **{accuracy*100:.2f}%**
""")

st.divider()

# =====================================================
# DETAIL EVALUASI
# =====================================================

st.subheader("Detail Perhitungan Accuracy")

st.dataframe(

    evaluasi[

        [

            "title",

            "rating",

            "content_warning",

            "Actual",

            "Prediction",

            "Status"

        ]

    ],

    use_container_width=True

)

st.caption("""
Keterangan:

Actual = Label sebenarnya pada dataset.

Prediction = Hasil prediksi sistem.

Status = Kesesuaian antara Actual dan Prediction.
""")

st.divider()

# =====================================================
# PIE CHART ACCURACY
# =====================================================

pie_accuracy = pd.DataFrame({

    "Kategori":[

        "Prediksi Benar",

        "Prediksi Salah"

    ],

    "Jumlah":[

        benar,

        salah

    ]

})

fig_acc = px.pie(

    pie_accuracy,

    values="Jumlah",

    names="Kategori",

    hole=0.45,

    title="Distribusi Accuracy"

)

fig_acc.update_layout(

    height=500

)

st.plotly_chart(

    fig_acc,

    use_container_width=True

)

st.divider()

# =====================================================
# INTERPRETASI
# =====================================================

st.subheader("Interpretasi Accuracy")

st.info(f"""

Accuracy sistem sebesar **{accuracy*100:.2f}%**.

Hal ini menunjukkan bahwa seluruh film yang direkomendasikan
berhasil memenuhi kriteria keamanan berdasarkan atribut
**content_warning** sehingga prediksi sistem sesuai dengan
label aktual pada dataset.

Dengan demikian proses Age Rating Filter,
Safety Filter, serta Weighted Product
berhasil menghasilkan rekomendasi film
yang aman untuk pengguna.

""")

# =====================================================
# RINGKASAN HASIL EVALUASI
# =====================================================

st.divider()

st.header("Ringkasan Hasil Evaluasi")

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
### Hasil Penyaringan

- Dataset Awal : **{jumlah_dataset}** film

- Lolos Age Rating Filter : **{jumlah_age}** film

- 🛡 Lolos Safety Filter : **{jumlah_safe}** film

- Top Recommendation : **{len(hasil)}** film
""")

with col2:

    st.success(f"""
### Hasil Evaluasi

- Accuracy : **{accuracy*100:.2f}%**

- Film Terbaik :
**{hasil.iloc[0]['title']}**

- IMDb Rating :
**{hasil.iloc[0]['imdb_rating']}**

- Nilai Vektor V :
**{hasil.iloc[0]['Vektor_V']:.4f}**
""")

st.divider()

# =====================================================
# ANALISIS HASIL
# =====================================================

st.header("Analisis Hasil")

st.markdown(f"""

Berdasarkan hasil evaluasi, sistem rekomendasi berhasil
melakukan proses penyaringan secara bertahap dimulai dari
**Age Rating Filter**, kemudian **Safety Filter**, hingga
dilakukan proses perangkingan menggunakan metode
**Weighted Product**.

Dari total **{jumlah_dataset}** film pada dataset,
sebanyak **{jumlah_age}** film memenuhi kategori usia
pengguna (**{umur} tahun**). Setelah dilakukan
Safety Filter menggunakan atribut **content_warning**,
tersisa **{jumlah_safe}** film yang dinyatakan aman.

Selanjutnya metode **Weighted Product**
menghasilkan **10 film rekomendasi terbaik**
berdasarkan kombinasi nilai
**Similarity Score** dan **IMDb Rating**.

Nilai Accuracy yang diperoleh sebesar
**{accuracy*100:.2f}%** menunjukkan bahwa seluruh
film hasil rekomendasi memiliki label keamanan
yang sesuai dengan data aktual pada dataset.

""")

st.divider()

# =====================================================
# KESIMPULAN
# =====================================================

st.header("Kesimpulan")

st.success(f"""

Berdasarkan hasil implementasi dan evaluasi sistem,
dapat disimpulkan bahwa:

Content-Based Filtering menggunakan
TF-IDF dan Cosine Similarity
berhasil menemukan kandidat film
yang memiliki kemiripan dengan film acuan.

Age Rating Filter berhasil
menyesuaikan rekomendasi berdasarkan
kategori usia pengguna.

Safety Filter berhasil
menghilangkan seluruh film yang memiliki
atribut **content_warning = True** sehingga
rekomendasi menjadi lebih aman.

Weighted Product berhasil melakukan
perangkingan berdasarkan nilai
Similarity Score dan IMDb Rating
untuk memperoleh film terbaik.

Sistem menghasilkan
**Top 10 rekomendasi film**
yang relevan dan aman
bagi pengguna anak di bawah umur.

Hasil evaluasi menunjukkan
Accuracy sebesar **{accuracy*100:.2f}%**
yang menunjukkan bahwa prediksi sistem
sesuai dengan label keamanan
yang terdapat pada dataset.

""")

st.balloons()