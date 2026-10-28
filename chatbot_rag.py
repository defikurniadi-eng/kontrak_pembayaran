import os
from dotenv import load_dotenv
from groq import Groq
from retriever import MesinPencari

# 1. Memuat konfigurasi API Key dari file .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key or "tempelkan" in api_key:
    print("[PERINGATAN] Mohon isi GROQ_API_KEY Anda di dalam file .env terlebih dahulu.")
    exit(1)

# 2. Inisialisasi Klien Groq dan Mesin Pencari Dokumen
client = Groq(api_key=api_key)
pencari = MesinPencari(folder="dokumen")

def tanya_rag(pertanyaan: str) -> str:
    """
    Alur RAG:
    1. Retrieval: Mencari dokumen relevan dari folder 'dokumen'
    2. Generation: Mengirimkan dokumen + pertanyaan ke LLM Groq
    """
    # Langkah A: Retrieval (Ambil 2 dokumen paling relevan)
    dokumen_relevan = pencari.cari(pertanyaan, top_k=2)
    
    if not dokumen_relevan:
        return "Maaf, tidak ditemukan dokumen yang relevan dengan pertanyaan Anda di arsip."

    # Gabungkan isi dokumen yang ditemukan menjadi 'contekan' (konteks)
    konteks_teks = ""
    for doc in dokumen_relevan:
        konteks_teks += f"\n--- SUMBER FILE: {doc['nama_file']} ---\n{doc['isi']}\n"

    # Langkah B: Prompt Engineering (Instruksi ketat agar AI tidak halusinasi)
    system_prompt = (
        "Anda adalah asisten AI pengelolaan dokumen yang profesional dan teliti.\n"
        "Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan konteks dokumen yang dilampirkan.\n"
        "Aturan ketat:\n"
        "- Jawab langsung ke intinya dengan bahasa Indonesia yang jelas dan formal.\n"
        "- Jika informasi tidak tertulis di dokumen, katakan bahwa data tidak ditemukan di dokumen.\n"
        "- Jangan mengarang data di luar dokumen.\n"
        "- Di akhir jawaban, wajib tuliskan nama file sumber dokumen yang Anda gunakan sebagai rujukan."
    )

    user_prompt = f"""Konteks Dokumen:
{konteks_teks}

Pertanyaan: {pertanyaan}

Jawaban:"""

    # Langkah C: Generation (Groq LLM)
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print("=" * 60)
    print("Selamat datang di Chatbot RAG Pengelolaan Dokumen!")
    print("Ketik pertanyaan Anda tentang kontrak/pembayaran.")
    print("Ketik 'keluar' untuk mengakhiri program.")
    print("=" * 60)

    while True:
        try:
            pertanyaan_user = input("\n[Anda]: ").strip()
            if not pertanyaan_user:
                continue
            if pertanyaan_user.lower() in ["keluar", "exit", "quit"]:
                print("Terima kasih telah menggunakan Chatbot RAG!")
                break

            print("\n[AI sedang mencari dokumen dan memproses jawaban...]")
            jawaban = tanya_rag(pertanyaan_user)
            print("-" * 60)
            print(f"[Jawaban AI]:\n{jawaban}")
            print("-" * 60)
        except (KeyboardInterrupt, EOFError):
            print("\nProgram dihentikan.")
            break
