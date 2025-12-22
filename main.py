from channels import CHANNELS
from channels_resolver import resolve_channel

SITE = "https://trgoals1495.xyz"

lines = ["#EXTM3U"]

for ch in CHANNELS:
    stream, ref = resolve_channel(SITE, ch["id"])

    if not stream:
        print(f"[!] Çözülmedi: {ch['name']}")
        continue

    lines.append(f'#EXTINF:-1,{ch["name"]}')
    lines.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0')
    lines.append(f'#EXTVLCOPT:http-referrer={ref}')
    lines.append(stream)

if len(lines) == 1:
    print("Playlist boş, çıkılıyor.")
    exit(1)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("[OK] playlist.m3u oluşturuldu")
