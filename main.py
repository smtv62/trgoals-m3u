from src.finder import find_active_site
from src.playlist import generate_m3u

def main():
    site = find_active_site()
    if not site:
        print("❌ Aktif site bulunamadı")
        return

    playlist = generate_m3u(site)

    if playlist.strip() == "#EXTM3U":
        print("⚠️ Hiç kanal çözülemedi")
        return

    with open("umitm0d.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print("🎉 Playlist hazır: umitm0d.m3u")

if __name__ == "__main__":
    main()
