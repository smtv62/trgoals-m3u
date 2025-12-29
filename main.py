import requests
import re
from channels import CHANNELS
from resolver import find_baseurl

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def find_active_site(start=1490, end=1700):
    for i in range(start, end + 1):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(
                site,
                headers=HEADERS,
                timeout=6,
                allow_redirects=False  # 🔴 EN KRİTİK SATIR
            )

            # redirect varsa ELİYORUZ
            if r.status_code in (301, 302, 307, 308):
                continue

            # gerçekten kendi domaini mi?
            if r.status_code == 200 and f"trgoals{i}.xyz" in r.text:
                # baseurl testi (asıl sağlam kontrol)
                test_base = find_baseurl(site, "yayin1")
                if test_base:
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
