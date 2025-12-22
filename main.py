import requests
import re
import sys
from channels import CHANNELS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "*/*",
    "Accept-Language": "tr-TR,tr;q=0.9",
}

def find_active_site():
    for i in range(1490, 1510):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(site, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                print(f"[OK] Aktif site: {site}")
                return site
        except:
            pass
    return None

def resolve_stream(site, channel_id):
    url = f"{site}/channel.html?id={channel_id}"

    headers = HEADERS.copy()
    headers["Referer"] = site + "/"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except:
        return None

    html = r.text

    # 🔥 EN SAĞLAM YÖNTEM → direkt m3u8 yakala
    m3u8 = re.search(r'https?://[^"\']+\.m3u8[^"\']*', html)
    if m3u8:
        return m3u8.group(0)

    return None

def main():
    site = find_active_site()
    if not site:
        print("[HATA] Aktif site bulunamadı")
        sys.exit(1)

    lines = ["#EXTM3U"]

    for ch in CHANNELS:
        stream = resolve_stream(site, ch["id"])
        if not stream:
            print(f"[!] Çözülmedi: {ch['name']}")
            continue

        lines.append(f'#EXTINF:-1,{ch["name"]}')
        lines.append(stream)

    if len(lines) == 1:
        print("Playlist boş, çıkılıyor.")
        sys.exit(1)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("[OK] playlist.m3u oluşturuldu")

if __name__ == "__main__":
    main()
