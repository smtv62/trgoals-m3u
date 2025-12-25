import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def find_active_site(start=3, end=50):
    for i in range(start, end + 1):
        site = f"https://tvdahibet{i}.com"
        try:
            r = requests.get(site, timeout=5)
            if r.status_code == 200:
                print(f"[OK] Aktif site: {site}")
                return site
        except:
            continue
    return None


def find_baseurl(site, channel_id):
    url = f"{site}/channel.html?id={channel_id}"
    headers = HEADERS.copy()
    headers["Referer"] = site + "/"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except:
        return None

    html = r.text

    # 1️⃣ data = {...} içinden baseurl çek
    data_match = re.search(r'data\s*=\s*({.*?});', html, re.DOTALL)
    if data_match:
        try:
            data_json = data_match.group(1)
            data = json.loads(data_json)
            if "baseurl" in data:
                return data["baseurl"].rstrip("/") + "/"
        except:
            pass

    # 2️⃣ fallback: direkt m3u8 varsa
    m3u8 = re.search(r'https?://[^"\']+\.m3u8', html)
    if m3u8:
        return m3u8.group(0).rsplit("/", 1)[0] + "/"

    return None
