from src.finder import find_active_site
from src.parser import find_base_url
from src.playlist import generate_m3u
import sys

def main():
    site = find_active_site()
  if not site:
    print("⚠️ Aktif TRGoals sitesi bulunamadı, çıkılıyor")
    return

    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    base_url = find_base_url(channel_url)
    if not base_url:
        print("Base URL bulunamadı")
        sys.exit(1)

    playlist = generate_m3u(base_url, site)
    with open("umitm0d.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print("Playlist güncellendi")

if __name__ == "__main__":
    main()
