import requests
from channels import CHANNELS
from resolver import find_baseurl

START = 1489       # burayı değiştirince artık SAĞLIKLI çalışır
END   = 1700

def find_active_site():
    for i in range(START, END + 1):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(site, timeout=5)
            if r.status_code != 200:
                continue

            # ASIL KRİTİK NOKTA
            baseurl = find_baseurl(site, "yayin1")
            if baseurl:
                print(f"[OK] Gerçek aktif site bulundu: {site}")
                return site, baseurl
            else:
                print(f"[!] Yayın yok, atlandı: {site}")

        except Exception:
            continue

    return None, None


def main():
    site, baseurl = find_active_site()

    if not site or not baseurl:
        print("[HATA] Aktif ve yayın veren site bulunamadı")
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
