# main.py
from src.finder import find_active_site
from src.parser import find_base_url
from src.playlist import generate_m3u

OUTPUT = "umitm0d.m3u"

def write_placeholder(reason):
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# ⚠️ Playlist üretilemedi: {reason}\n")

def main():
    print("▶️ TRGoals M3U Generator başlatıldı")

    site = find_active_site()
    if not site:
        print("⚠️ Aktif site bulunamadı")
        write_placeholder("Aktif site bulunamadı")
        return

    print(f"✅ Aktif site bulundu: {site}")

    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    base_url = find_base_url(channel_url)
    if not base_url:
        print("⚠️ Base URL bulunamadı")
        write_placeholder("Base URL bulunamadı")
        return

    print(f"✅ Base URL bulundu: {base_url}")

    playlist = generate_m3u(base_url, site)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"🎉 Playlist oluşturuldu: {OUTPUT}")

if __name__ == "__main__":
    main()
