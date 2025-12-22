import requests
import re
from channels import CHANNELS

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def find_baseurl(site):
    test_url = f"{site}/channel.html?id=yayin1"
    r = requests.get(test_url, headers={
        **HEADERS,
        "Referer": site + "/"
    }, timeout=10)

    # View Source içinden baseurl yakala
    m = re.search(r'(https?://[^"\']+/)yayin1\.m3u8', r.text)
    if m:
        return m.group(1)

    return None


def main():
    site = "https://trgoals1495.xyz"
    print(f"[OK] Aktif site: {site}")

    baseurl = find_baseurl(site)
    if not baseurl:
        print("[HATA] BaseURL bulunamadı")
        return

    lines = ["#EXTM3U"]

    for ch in CHANNELS:
        stream = baseurl.rstrip("/") + "/" + ch["file"]

        lines.append(
            f'#EXTINF:-1 tvg-id="{ch["tvg_id"]}",{ch["name"]}'
        )
        lines.append(f"#EXTVLCOPT:http-referrer={site}/")
        lines.append(f"#EXTVLCOPT:http-user-agent=Mozilla/5.0")
        lines.append(stream)

        print(f"[OK] Eklendi: {ch['name']}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("[OK] playlist.m3u oluşturuldu")


if __name__ == "__main__":
    main()
