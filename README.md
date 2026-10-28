# 📄 Chatbot AI Pengelolaan Dokumen (RAG)

Aplikasi Chatbot berbasis **Retrieval-Augmented Generation (RAG)** untuk mencari dan menjawab informasi spesifik terkait dokumen administrasi kantor (Surat Kontrak dan Bukti Pembayaran).

---

## 🛠️ Arsitektur & Teknologi

* **Generator (LLM)**: [Groq API](https://groq.com) menggunakan model `openai/gpt-oss-120b` (sangat cepat dan akurat).
* **Retriever (Mesin Pencari)**: `rank-bm25` (Algoritma BM25Plus untuk pencarian kata kunci presisi pada nomor kontrak, kode transaksi, dan termin).
* **Penyimpanan Dokumen**: File arsip lokal di dalam folder `dokumen/`.
* **Bahasa Pemrograman**: Python 3.15.

---

## 🚀 Cara Menjalankan Aplikasi

### Cara Paling Mudah (Tanpa Command Prompt)
Cukup buka folder `d:\Belajar AI2` di File Explorer Windows Anda, lalu **klik ganda (double-click)** pada file:
👉 **`Jalankan_Chatbot.bat`**

Peramban web (Chrome/Edge) Anda akan langsung terbuka secara otomatis menampilkan antarmuka chat website yang rapi dan mudah digunakan.

---

### Cara Melalui Terminal (Opsional)
Jika Anda ingin menjalankannya lewat terminal:
```bash
# Menjalankan versi Website:
python app.py

# Atau menjalankan versi teks terminal:
python chatbot_rag.py
```

---

## 🧪 Rangkuman Hasil Pengujian

| No | Pertanyaan Uji | Hasil Pencarian | Ketepatan Jawaban | Status |
|---|---|---|---|:---:|
| 1 | Nomor & nilai kontrak pengadaan laptop | `kontrak_045_pengadaan_laptop.txt` | Menjawab no `045/SPK-IT/ABC/2024` dan total Rp 721.500.000,- lengkap (DPP + PPN). | ✅ Lolos |
| 2 | Periode waktu pelaksanaan kontrak | `kontrak_045_pengadaan_laptop.txt` | Menjawab periode 1 Maret 2024 s/d 31 Mei 2024 (90 hari). | ✅ Lolos |
| 3 | Riwayat realisasi pembayaran laptop | `pembayaran_045_termin_1.txt` & `pembayaran_045_termin_2.txt` | Menjawab 2 termin pembayaran lengkap dengan tanggal dan nominal. | ✅ Lolos |
| 4 | Kasus data tidak ada (kontrak tenaga kerja) | `kontrak_045_pengadaan_laptop.txt` | AI menolak mengarang dan menyatakan data tidak ditemukan. | ✅ Lolos |

---

## ⚠️ Keterbatasan Sistem Saat Ini

1. **Format Dokumen**: Saat ini masih membaca file teks `.txt` langsung, belum mencakup pembacaan file PDF hasil scan (OCR).
2. **Kalkulasi Matematis**: Jika diminta menjumlahkan total puluhan pembayaran, AI bergantung pada penalaran teks LLM, bukan perhitungan database SQL.
3. **Antarmuka Pengguna (UI)**: Interaksi saat ini masih berbasis baris perintah (Terminal/CLI).

---

## 💡 Rekomendasi Pengembangan Selanjutnya

1. **Dukungan Format PDF**: Integrasikan library `pypdf` atau `pdfplumber` agar sistem dapat otomatis membaca file dokumen berformat PDF.
2. **Antarmuka Grafis (Web UI)**: Bangun antarmuka web sederhana yang ramah pengguna menggunakan **Streamlit** agar pengguna non-teknis bisa langsung mengunggah dokumen lewat browser.
3. **Ekstraksi Metadata Terstruktur**: Tambahkan tabel metadata (misal SQLite) untuk mencatat nomor kontrak dan nominal secara terstruktur untuk mempermudah perhitungan laporan keuangan.

