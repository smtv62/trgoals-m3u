# main.py
from src.finder import find_active_site
from src.playlist import generate_m3u

OUTPUT = "umitm0d.m3u"

def main():
    print("▶️ TRGoals M3U Generator başlatıldı")

    site = find_active_site()
    if not site:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n# ⚠️ Aktif site bulunamadı\n")
        print("⚠️ Aktif site bulunamadı")
        return

    print(f"✅ Aktif site bulundu: {site}")

    # 🔥 ARTIK BASE_URL = SİTENİN KENDİSİ
    base_url = site.rstrip("/") + "/"

    playlist = generate_m3u(base_url, site)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"🎉 Playlist oluşturuldu: {OUTPUT}")
    print(f"🔗 Base URL: {base_url}")

if __name__ == "__main__":
    main()
