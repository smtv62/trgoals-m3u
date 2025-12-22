from channels import CHANNELS
from baseurl_finder import find_baseurl

SITE = "https://trgoals1495.xyz"

print(f"[OK] Aktif site: {SITE}")

baseurl = find_baseurl(SITE)
if not baseurl:
    print("[HATA] BaseURL bulunamadı")
    exit(1)

print(f"[OK] BaseURL bulundu: {baseurl}")

lines = ["#EXTM3U"]

for ch in CHANNELS:
    stream = baseurl.rstrip("/") + "/" + ch["file"]
    lines.append(f"#EXTINF:-1,{ch['name']}")
    lines.append(stream)
    print(f"  ✔ {ch['name']}")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("[OK] playlist.m3u oluşturuldu")
