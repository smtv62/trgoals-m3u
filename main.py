from channels import CHANNELS
from finder import find_active_site, find_baseurl

SITE = find_active_site()
if not SITE:
    print("Aktif site bulunamadı")
    exit(1)

baseurl = find_baseurl(SITE)
if not baseurl:
    print("Base URL bulunamadı")
    exit(1)

lines = ["#EXTM3U"]

for ch in CHANNELS:
    stream = baseurl.rstrip("/") + "/" + ch["file"]

    lines.append(
        f'#EXTINF:-1,{ch["name"]}\n'
        f'#EXTVLCOPT:http-user-agent=Mozilla/5.0\n'
        f'#EXTVLCOPT:http-referrer={SITE}/\n'
        f'{stream}'
    )

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("[OK] playlist.m3u oluşturuldu")
