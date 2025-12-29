import requests
from channels import CHANNELS
from resolver import find_baseurl

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def find_active_site(start=1488, end=1700):
    for i in range(start, end + 1):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(
                site,
                headers=HEADERS,
                timeout=6,
                allow_redirects=False   # 🔴 EN ÖNEMLİ SATIR
            )

            # Redirect varsa → bu domaini geç
            if r.status_code in (301, 302, 303, 307, 308):
                print(f"[SKIP] Redirect var: {site}")
                continue

            # Gerçek içerik mi?
            if r.status_code == 200 and "channel.html" in r.text:
                print(f"[OK] Aktif site bulundu: {site}")
                return site

        except Exception as e:
            continue

    return None


def main():
    site = find_active_site(start=1495, end=1700)
    if not site:
        print("[HATA] Aktif site bulunamadı")
        return

    baseurl = find_baseurl(site, "id=yayin1")
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
