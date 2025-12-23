import sys
import requests
from channels_resolver import resolve_channel
from channels import CHANNELS

START_DOMAIN = 1495
END_DOMAIN = 1700

def find_active_site():
    for i in range(START_DOMAIN, END_DOMAIN + 1):
        url = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return url
        except:
            continue
    return None

def main():
    site = find_active_site()
    if not site:
        print("[HATA] Aktif site bulunamadı.")
        sys.exit(1)

    print(f"[OK] Aktif site: {site}")

    playlist_lines = ["#EXTM3U"]
    found = False

    for ch in CHANNELS:
        stream = resolve_channel(site, ch["id"])
        if stream:
            found = True
            playlist_lines.append(f'#EXTINF:-1,{ch["name"]}')
            playlist_lines.append(stream)
            print(f"[OK] Çözüldü: {ch['name']}")
        else:
            print(f"[!] Çözülmedi: {ch['name']}")

    if not found:
        print("Playlist boş, çıkılıyor.")
        sys.exit(1)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(playlist_lines))
    print("Playlist oluşturuldu: playlist.m3u")

if __name__ == "__main__":
    main()
