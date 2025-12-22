from channels import CHANNELS
from resolver import get_baseurl

SITE = "https://trgoals1495.xyz"
OUTPUT = "playlist.m3u"

print(f"[OK] Aktif site: {SITE}")

baseurl = get_baseurl(SITE)

if not baseurl:
    print("[HATA] BaseURL bulunamadı")
    exit(1)

lines = ["#EXTM3U"]

for ch in CHANNELS:
    stream = baseurl.rstrip("/") + "/" + ch["file"]

    lines.append(f"#EXTINF:-1,{ch['name']}")
    lines.append(stream)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[OK] {OUTPUT} oluşturuldu")
