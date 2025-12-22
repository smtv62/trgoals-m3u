from channels import CHANNELS
from channels_resolver import resolve_channel

SITE = "https://trgoals1494.xyz"

lines = ["#EXTM3U"]

for ch in CHANNELS:
    url = resolve_channel(SITE, ch["id"])
    if not url:
        print(f"[!] Çözülmedi: {ch['name']}")
        continue

    lines.append(f"#EXTINF:-1,{ch['name']}")
    lines.append(url)

if len(lines) == 1:
    print("Playlist boş, çıkılıyor.")
    exit(1)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("[OK] playlist.m3u oluşturuldu")
