from channels import CHANNELS
from channels_resolver import resolve_channel

# 🔁 Aktif site güncellendi
SITE = "https://trgoals1495.xyz"

lines = ["#EXTM3U"]

print(f"[OK] Aktif site: {SITE}")

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
    exit(1)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("[OK] playlist.m3u oluşturuldu")
