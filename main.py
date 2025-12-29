import requests
from channels import CHANNELS
from resolver import find_baseurl

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://google.com/"
}

START_DOMAIN = 1489
END_DOMAIN = 1700


def find_active_site():
    """
    GERÇEK aktif domaini bulur.
    channel.html?id=yayin1 çalışmıyorsa domain ELENİR
    """
    for i in range(START_DOMAIN, END_DOMAIN + 1):
        site = f"https://trgoals{i}.xyz"
        test_url = f"{site}/channel.html?id=yayin1"

        try:
            r = requests.get(test_url, headers=HEADERS, timeout=7)
            if r.status_code == 200 and "iframe" in r.text:
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
