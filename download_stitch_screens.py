import os
import json
import base64
import httpx

PROJECT_ID = "3570232672003983256"
API_KEY = os.getenv("GCP_API_KEY", "")
BASE_URL = "https://stitch.googleapis.com/v1"
HEADERS = {"X-Goog-Api-Key": API_KEY}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "stitch_designs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_SCREENS = [
    {"id": "a0feaae0f9864b16bea44c88611da401", "name": "dashboard_manajemen_kontrak_bsp"},
    {"id": "21332def0e234db08d0f4261bf3d1e37", "name": "redesain_chatbot_arsip_kontrak_bsp"},
    {"id": "15926905206630221187", "name": "log_jpeg"},
    {"id": "15926905206630220073", "name": "chatbot_tampilan_png"}
]

def fetch_and_save_screen(screen_info):
    screen_id = screen_info["id"]
    file_name_prefix = screen_info["name"]
    print(f"\n[+] Memproses Layar: {file_name_prefix} (ID: {screen_id})")

    # 1. Dapatkan detail layar (metadata)
    detail_url = f"{BASE_URL}/projects/{PROJECT_ID}/screens/{screen_id}"
    res = httpx.get(detail_url, headers=HEADERS, timeout=30.0)
    
    if res.status_code != 200:
        print(f"[-] Gagal mendapatkan detail layar {screen_id}: {res.status_code} {res.text}")
        return

    data = res.json()
    title = data.get("title", file_name_prefix)
    print(f"    Judul Desain: {title}")

    # Simpan metadata JSON
    meta_path = os.path.join(OUTPUT_DIR, f"{file_name_prefix}_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # 2. Unduh Kode HTML jika tersedia
    if "htmlCode" in data and "downloadUrl" in data["htmlCode"]:
        html_url = data["htmlCode"]["downloadUrl"]
        print(f"    Mengunduh kode HTML...")
        r_html = httpx.get(html_url, headers=HEADERS, timeout=30.0)
        if r_html.status_code == 200:
            try:
                html_json = r_html.json()
                html_content = html_json.get("dataString", "")
            except Exception:
                html_content = r_html.text
            
            html_path = os.path.join(OUTPUT_DIR, f"{file_name_prefix}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"    [OK] File HTML tersimpan di: {html_path}")
        else:
            print(f"    [-] Gagal mengunduh HTML: {r_html.status_code}")

    # 3. Unduh Gambar / Screenshot jika tersedia
    if "screenshot" in data and "downloadUrl" in data["screenshot"]:
        img_url = data["screenshot"]["downloadUrl"]
        print(f"    Mengunduh gambar screenshot...")
        r_img = httpx.get(img_url, headers=HEADERS, timeout=60.0)
        if r_img.status_code == 200:
            try:
                img_json = r_img.json()
                img_bytes = base64.b64decode(img_json.get("dataString", ""))
            except Exception:
                img_bytes = r_img.content
            
            ext = "png"
            if "jpeg" in file_name_prefix:
                ext = "jpg"
            
            img_path = os.path.join(OUTPUT_DIR, f"{file_name_prefix}.{ext}")
            with open(img_path, "wb") as f:
                f.write(img_bytes)
            print(f"    [OK] File Gambar tersimpan di: {img_path} ({len(img_bytes)} bytes)")
        else:
            print(f"    [-] Gagal mengunduh screenshot: {r_img.status_code}")

if __name__ == "__main__":
    print("=" * 60)
    print("MENGUNDUH ASET DESAIN DARI GOOGLE STITCH")
    print(f"Project ID: {PROJECT_ID}")
    print("=" * 60)
    
    for s in TARGET_SCREENS:
        fetch_and_save_screen(s)

    print("\n" + "=" * 60)
    print("Semua aset Stitch telah selesai diunduh!")
    print(f"Folder penyimpanan: {OUTPUT_DIR}")
    print("=" * 60)

