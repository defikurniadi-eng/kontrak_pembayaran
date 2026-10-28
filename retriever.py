import os
import re
from rank_bm25 import BM25Plus

# Folder tempat dokumen kontrak dan pembayaran disimpan
FOLDER_DOKUMEN = "dokumen"

def bersihkan_teks(teks: str) -> list[str]:
    """
    Memecah teks kalimat menjadi daftar kata-kata kecil (token)
    agar mudah dicocokkan oleh algoritma pencari.
    """
    return re.findall(r"\w+", teks.lower())

def muat_semua_dokumen(folder: str = FOLDER_DOKUMEN):
    """
    Membaca seluruh file teks di dalam folder dokumen.
    """
    daftar_dokumen = []
    for nama_file in os.listdir(folder):
        if nama_file.endswith(".txt"):
            path_file = os.path.join(folder, nama_file)
            with open(path_file, "r", encoding="utf-8") as f:
                isi = f.read()
                daftar_dokumen.append({
                    "nama_file": nama_file,
                    "isi": isi,
                    "tokens": bersihkan_teks(isi)
                })
    return daftar_dokumen

class MesinPencari:
    def __init__(self, folder: str = FOLDER_DOKUMEN):
        # 1. Muat dokumen
        self.dokumen = muat_semua_dokumen(folder)
        # 2. Bangun indeks pencarian BM25Plus (sangat handal untuk data sedikit maupun banyak)
        korpus = [doc["tokens"] for doc in self.dokumen]
        self.bm25 = BM25Plus(korpus)

    def cari(self, query: str, top_k: int = 3):
        """
        Mencari dokumen yang paling relevan dengan pertanyaan user.
        top_k: jumlah dokumen teratas yang ingin diambil.
        """
        query_tokens = bersihkan_teks(query)
        skor = self.bm25.get_scores(query_tokens)
        
        # Urutkan dokumen dari nilai kecocokan (skor) tertinggi
        indeks_tertinggi = sorted(range(len(skor)), key=lambda i: skor[i], reverse=True)
        
        hasil = []
        for i in indeks_tertinggi[:top_k]:
            if skor[i] > 0:
                hasil.append({
                    "nama_file": self.dokumen[i]["nama_file"],
                    "isi": self.dokumen[i]["isi"],
                    "skor": skor[i]
                })
        return hasil

if __name__ == "__main__":
    print("=== MENGUJI MESIN PENCARI DOKUMEN ===")
    mesin = MesinPencari()
    
    # Contoh uji coba pencarian
    pertanyaan_uji = "Berapa nomor kontrak untuk pengadaan laptop?"
    print(f"Pertanyaan: '{pertanyaan_uji}'\n")
    
    hasil = mesin.cari(pertanyaan_uji, top_k=1)
    for h in hasil:
        print(f"[DOKUMEN DITEMUKAN]: {h['nama_file']} (Skor Relevansi: {h['skor']:.2f})")
        print("Ringkasan isi:")
        print(h["isi"][:200] + "...\n")

