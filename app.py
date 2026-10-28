import os
import webbrowser
import threading
from flask import Flask, render_template, request, jsonify
from chatbot_rag import tanya_rag

app = Flask(__name__)

@app.route("/")
def beranda():
    return render_template("index.html")

@app.route("/tanya", methods=["POST"])
def tanya():
    try:
        data = request.get_json() or {}
        pertanyaan = data.get("pertanyaan", "").strip()
        
        if not pertanyaan:
            return jsonify({"jawaban": "Pertanyaan tidak boleh kosong."})
        
        jawaban = tanya_rag(pertanyaan)
        return jsonify({"jawaban": jawaban})
    except Exception as e:
        print(f"\n[ERROR SERVER]: {e}\n")
        return jsonify({"jawaban": f"Terjadi kendala pada sistem: {str(e)}"}), 200

def buka_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("=" * 60)
    print("Memulai Server Website Chatbot RAG...")
    print("Website akan otomatis terbuka di peramban (browser) Anda.")
    print("Alamat lokal: http://127.0.0.1:5000")
    print("=" * 60)

    # Otomatis buka browser setelah 1.2 detik
    threading.Timer(1.2, buka_browser).start()
    
    # Jalankan server Flask lokal
    app.run(host="127.0.0.1", port=5000, debug=False)
