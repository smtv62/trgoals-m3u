from channels import CHANNELS
from resolver import resolve_channel
import sys

OUTPUT_FILE = "playlist.m3u"
SITE = "https://trgoals1494.xyz"

def main():
    lines = ["#EXTM3U"]

    for ch in CHANNELS:
        print(f"[+] Çözülüyor: {ch['name']}")
        stream = resolve_channel(SITE, ch["id"])

        if not stream:
            print(f"[!] Çözülmedi: {ch['name']}")
            continue

        lines.append(
            f'#EXTINF:-1 tvg-id="{ch["tvg_id"]}",{ch["name"]}'
        )
        lines.append("#EXTVLCOPT:http-user-agent=Mozilla/5.0")
        lines.append(f"#EXTVLCOPT:http-referrer={SITE}")
        lines.append(stream)

    if len(lines) == 1:
        print("Playlist boş, çıkılıyor.")
        sys.exit(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Playlist oluşturuldu → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
