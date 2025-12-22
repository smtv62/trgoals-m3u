import requests
from channels import CHANNELS
from resolver import find_baseurl

def find_active_site():
    for i in range(1495, 1600):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(site, timeout=5)
            if r.status_code == 200 and "channel.html" in r.text:
                print(f"[OK] Aktif site: {site}")
                return site
        except:
            continue
    return None

def main():
    site = find_active_site()
    if not site:
        print("[HATA] Aktif site bulunamadı")
        return

    baseurl = find_baseurl(site, "yayin1")
    if not baseurl:
        print("[HATA] BaseURL bulunamadı")
        return

    lines = ["#EXTM3U"]

    for ch in CHANNELS:
        stream = baseurl.rstrip("/") + "/" + ch["file"]

        lines.append(f'#EXTINF:-1,{ch["name"]}')
        lines.append(f'#EXTVLCOPT:http-referrer={site}/')
        lines.append(stream)

        print(f"[OK] Eklendi: {ch['name']}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("[OK] playlist.m3u oluşturuldu")

if __name__ == "__main__":
    main()
