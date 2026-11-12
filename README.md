
# Sistem Rekomendasi Film Hybrid Menggunakan Content-Based Filtering dan Weighted Product

## 1. Deskripsi Proyek

Proyek ini merupakan pengembangan sistem rekomendasi film berbasis pendekatan *Hybrid Recommendation System* yang menggabungkan metode **Content-Based Filtering (CBF)** dan **Weighted Product (WP)**.

Sistem ini bertujuan untuk menghasilkan rekomendasi film berdasarkan kemiripan karakteristik film serta proses pemeringkatan berdasarkan kriteria dan bobot yang telah ditentukan.

Selain itu, sistem dilengkapi dengan mekanisme penyaringan berdasarkan kategori usia (*Age Rating Filter*) dan informasi peringatan konten (*Safety Filter*) untuk membantu pengguna memperoleh rekomendasi film yang sesuai dengan preferensi dan batasan yang ditentukan.

Aplikasi dikembangkan menggunakan Python dengan Streamlit sebagai antarmuka pengguna.

## 2. Tujuan Penelitian

1. Mengembangkan sistem rekomendasi film menggunakan pendekatan hybrid.
2. Menerapkan metode Content-Based Filtering untuk menghitung kemiripan antarfilm.
3. Menerapkan metode Weighted Product untuk melakukan pemeringkatan rekomendasi film.
4. Mengimplementasikan Age Rating Filter untuk menyaring film berdasarkan kategori usia.
5. Mengimplementasikan Safety Filter berdasarkan informasi content warning.
6. Menyediakan visualisasi dataset untuk mengetahui karakteristik data film yang digunakan.

## 3. Metode yang Digunakan

### 3.1 Content-Based Filtering (CBF)

Content-Based Filtering merupakan metode rekomendasi yang menghasilkan rekomendasi berdasarkan karakteristik atau atribut dari suatu item.

Tahapan yang digunakan:

- **Feature Engineering:** Mengolah atribut dataset film menjadi fitur yang dapat digunakan dalam proses rekomendasi.
- **TF-IDF:** Mengubah informasi tekstual film menjadi representasi numerik.
- **Cosine Similarity:** Menghitung tingkat kemiripan antarfilm berdasarkan representasi vektor TF-IDF.

### 3.2 Age Rating Filter

Age Rating Filter digunakan untuk menyaring film berdasarkan kategori batasan usia agar film yang direkomendasikan sesuai dengan kriteria usia pengguna.

### 3.3 Safety Filter

Safety Filter digunakan untuk melakukan penyaringan film berdasarkan informasi `content_warning`. Mekanisme ini membantu mengidentifikasi film yang memiliki peringatan konten tertentu.

### 3.4 Weighted Product (WP)

Weighted Product merupakan metode pengambilan keputusan multikriteria yang digunakan untuk melakukan pemeringkatan alternatif berdasarkan nilai kriteria dan bobot yang telah ditentukan.

Dalam sistem ini, Weighted Product digunakan untuk menghitung nilai preferensi film sehingga menghasilkan urutan rekomendasi berdasarkan prioritas kriteria yang diterapkan.

## 4. Alur Sistem

```text
Dataset Film
     |
     v
Data Preprocessing
     |
     v
Feature Engineering
     |
     v
TF-IDF
     |
     v
Cosine Similarity
     |
     v
Age Rating Filter
     |
     v
Safety Filter
(content_warning)
     |
     v
Weighted Product
     |
     v
Ranking Rekomendasi
     |
     v
Top 10 Rekomendasi Film
```

## 5. Fitur Sistem

- **Rekomendasi Film:** Menghasilkan rekomendasi berdasarkan kemiripan karakteristik film.
- **Content-Based Filtering:** Menggunakan TF-IDF dan Cosine Similarity untuk menghitung kemiripan antarfilm.
- **Age Rating Filter:** Menyaring film berdasarkan kategori usia.
- **Safety Filter:** Menyaring film berdasarkan informasi content warning.
- **Weighted Product:** Melakukan pemeringkatan film berdasarkan kriteria dan bobot.
- **Top 10 Rekomendasi:** Menampilkan sepuluh film dengan nilai preferensi tertinggi.
- **Visualisasi Dataset:** Menampilkan distribusi age rating, content warning, IMDb rating, serta daftar film dengan IMDb rating tertinggi.
- **Evaluasi Sistem:** Menyediakan pengujian terhadap hasil rekomendasi dan mekanisme penyaringan.

## 6. Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Pandas | Pengolahan dan manipulasi dataset |
| NumPy | Operasi komputasi numerik |
| Scikit-learn | Implementasi TF-IDF dan Cosine Similarity |
| Streamlit | Pengembangan antarmuka aplikasi |
| Plotly | Visualisasi data dan grafik |

## 7. Struktur Proyek

Struktur direktori proyek secara umum adalah sebagai berikut:

```text
movie-recommendation-hybrid-cbf-wp/
|
|-- app.py
|
|-- model/
|   |-- eda.py
|   |-- ...
|
|-- pages/
|   |-- visualisasi.py
|   |-- ...
|
|-- data/
|   |-- ...
|
|-- requirements.txt
|
|-- README.md
```

## 8. Instalasi dan Menjalankan Aplikasi

### 8.1 Clone Repository

```bash
git clone https://github.com/zidanazarya-glitch/movie-recommendation-hybrid-cbf-wp.git
```

### 8.2 Masuk ke Direktori Proyek

```bash
cd movie-recommendation-hybrid-cbf-wp
```

### 8.3 Membuat Virtual Environment

```bash
python -m venv venv
```

Aktifkan virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux atau macOS:**

```bash
source venv/bin/activate
```

### 8.4 Menginstal Dependencies

```bash
pip install -r requirements.txt
```

### 8.5 Menjalankan Aplikasi

```bash
streamlit run app.py
```

Setelah aplikasi berhasil dijalankan, Streamlit akan menampilkan alamat lokal yang dapat dibuka melalui browser.

## 9. Visualisasi Dataset

Sistem menyediakan halaman visualisasi dataset untuk memberikan gambaran mengenai karakteristik data film yang digunakan dalam penelitian.

Visualisasi yang disediakan meliputi:

1. Jumlah keseluruhan film dalam dataset.
2. Jumlah kategori age rating.
3. Rata-rata IMDb rating.
4. Distribusi kategori age rating.
5. Distribusi content warning.
6. Distribusi IMDb rating.
7. Sepuluh film dengan IMDb rating tertinggi.
8. Ringkasan dataset.

## 10. Evaluasi Sistem

Evaluasi dilakukan untuk mengetahui hasil pengujian sistem rekomendasi dan mekanisme penyaringan film.

Salah satu metode evaluasi yang digunakan adalah Confusion Matrix dengan komponen sebagai berikut:

- True Positive (TP)
- True Negative (TN)
- False Positive (FP)
- False Negative (FN)

Metrik evaluasi yang dapat dihitung meliputi:

- Accuracy
- Precision
- Recall
- F1-Score

Interpretasi hasil evaluasi perlu mempertimbangkan sumber pembentukan label ground truth. Apabila label ground truth dibentuk menggunakan aturan penyaringan yang sama dengan sistem, hasil evaluasi lebih tepat digunakan untuk mengukur konsistensi penerapan aturan penyaringan, bukan sebagai bukti akurasi prediksi independen.

## 11. Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari penelitian dan penyusunan skripsi.
