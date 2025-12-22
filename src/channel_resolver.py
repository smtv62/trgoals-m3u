# src/channel_resolver.py
import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": ""
}

def resolve_from_channel(site, channel_id):
    """
    channel.html içinden GERÇEK CDN m3u8 adresini çözer
    """
    url = f"{site.rstrip('/')}/channel.html?id={channel_id}"
    HEADERS["Referer"] = site

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return None

    html = r.text

    # 1️⃣ baseurl'u yakala
    base = re.search(r'const\s+baseurl\s*=\s*["\']([^"\']+)["\']', html)
    if not base:
        return None

    baseurl = base.group(1).rstrip("/")

    # 2️⃣ GERÇEK m3u8
    real_stream = f"{baseurl}/{channel_id}.m3u8"
    return real_stream
