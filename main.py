from channels import CHANNELS
from channels_resolver import resolve_channel

SITE = "https://trgoals1495.xyz"
OUTPUT = "playlist.m3u"

lines = ["#EXTM3U"]

print(f"[OK] Aktif site: {SITE}")

for ch in CHANNELS:
    stream = resolve_channel(SITE, ch["id"])

    if not stream:
        print(f"[!] Çözülmedi: {ch['name']}")
        continue

    lines.append(f"#EXTINF:-1,{ch['name']}")
    lines.append(stream)
    print(f"[OK] Çözüldü: {ch['name']}")

if len(lines) == 1:
    print("Playlist boş, çıkılıyor.")
    exit(1)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[OK] {OUTPUT} oluşturuldu")
