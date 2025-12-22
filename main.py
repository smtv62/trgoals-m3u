from channels import CHANNELS
from resolver import resolve_stream

SITE = "https://trgoals1494.xyz"
OUTPUT = "playlist.m3u"

lines = ["#EXTM3U"]

print(f"[OK] Aktif site: {SITE}")

for ch in CHANNELS:
    stream, referer = resolve_stream(SITE, ch["id"])

    if not stream:
        print(f"[!] Çözülmedi: {ch['name']}")
        continue

    print(f"[✓] Çözüldü: {ch['name']}")

    lines.append(f'#EXTINF:-1,{ch["name"]}')
    lines.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0')
    lines.append(f'#EXTVLCOPT:http-referrer={referer}')
    lines.append(stream)

if len(lines) == 1:
    print("Playlist boş, çıkılıyor.")
    exit(1)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[OK] {OUTPUT} oluşturuldu")
