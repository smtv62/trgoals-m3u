from channels import CHANNELS
from resolver import resolve_channel
import sys
import os

SITE = "https://trgoals1495.xyz"
OUTPUT = "playlist.m3u"

print(f"[OK] Aktif site: {SITE}")

lines = ["#EXTM3U"]

for ch in CHANNELS:
    url = resolve_channel(SITE, ch["id"])
    if not url:
        print(f"[!] Çözülmedi: {ch['name']}")
        continue

    lines.append(f"#EXTINF:-1,{ch['name']}")
    lines.append(url)
    print(f"[+] Eklendi: {ch['name']}")

if len(lines) == 1:
    print("Playlist boş, çıkılıyor.")
    sys.exit(1)

with open(os.path.join(os.getcwd(), OUTPUT), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[OK] {OUTPUT} oluşturuldu")
