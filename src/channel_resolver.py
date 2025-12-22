import re
import requests
import base64

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def resolve_from_channel(site, channel_id):
    url = f"{site.rstrip('/')}/channel.html?id={channel_id}"
    HEADERS["Referer"] = site

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return None

    html = r.text

    # 1️⃣ Direkt m3u8
    m3u8 = re.search(r'(https?://[^"\']+\.m3u8)', html)
    if m3u8:
        return m3u8.group(1)

    # 2️⃣ JS source
    src = re.search(r'source\s*[:=]\s*["\']([^"\']+)["\']', html)
    if src:
        return src.group(1)

    # 3️⃣ base64
    b64 = re.search(r'atob\(["\']([^"\']+)["\']\)', html)
    if b64:
        try:
            return base64.b64decode(b64.group(1)).decode()
        except Exception:
            pass

    return None
