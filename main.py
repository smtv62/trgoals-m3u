from channels import CHANNELS
from resolver import resolve_baseurl
import sys

SITE = "https://trgoals1495.xyz"

def main():
    print(f"[OK] Aktif site: {SITE}")

    lines = ["#EXTM3U"]

    for ch in CHANNELS:
        baseurl = resolve_baseurl(SITE, ch["id"])
        if not baseurl:
            print(f"[!] Çözülmedi: {ch['name']}")
            continue

        stream = baseurl.rstrip("/") + "/" + ch["file"]

        lines.append(f'#EXTINF:-1,{ch["name"]}')
        lines.append(f'#EXTVLCOPT:http-referrer={SITE}/')
        lines.append(stream)

    if len(lines) == 1:
        print("Playlist boş, çıkılıyor.")
        sys.exit(1)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("[OK] playlist.m3u oluşturuldu")

if __name__ == "__main__":
    main()
