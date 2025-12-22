# main.py
from src.finder import find_active_site
from src.parser import find_base_url
from src.playlist import generate_m3u
import sys

def main():
    site = find_active_site()
    if not site:
        print("⚠️ Aktif TRGoals sitesi bulunamadı. Çıkılıyor.")
        return

    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    base_url = find_base_url(channel_url)
    if not base_url:
        print("⚠️ Base URL bulunamadı. Çıkılıyor.")
        return

    playlist = generate_m3u(base_url, site)

    try:
        with open("umitm0d.m3u", "w", encoding="utf-8") as f:
            f.write(playlist)
    except OSError as e:
        print(f"❌ Dosya yazma hatası: {e}")
        return

    print(f"✅ Playlist başarıyla güncellendi → {base_url}")

if __name__ == "__main__":
    main()
