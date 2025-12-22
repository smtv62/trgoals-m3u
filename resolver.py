import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def resolve_stream(site, channel_id):
    channel_url = f"{site}/channel.html?id={channel_id}"

    headers = HEADERS.copy()
    headers["Referer"] = site + "/"

    try:
        r = requests.get(channel_url, headers=headers, timeout=10)
        r.raise_for_status()
    except:
        return None, None

    html = r.text

    # 1️⃣ iframe varsa içine gir
    iframe = re.search(r'<iframe[^>]+src=["\']([^"\']+)["\']', html)
    if iframe:
        iframe_url = iframe.group(1)
        if iframe_url.startswith("/"):
            iframe_url = site + iframe_url

        headers["Referer"] = channel_url
        try:
            r = requests.get(iframe_url, headers=headers, timeout=10)
            r.raise_for_status()
            html = r.text
        except:
            pass

    # 2️⃣ baseurl + m3u8 pattern
    baseurl = re.search(r'(https?://[^"\']+?/)', html)
    m3u8 = re.search(r'([a-zA-Z0-9_/.-]+\.m3u8)', html)

    if baseurl and m3u8:
        stream = baseurl.group(1) + m3u8.group(1)
        return stream, channel_url

    # 3️⃣ fallback: direkt full m3u8
    direct = re.search(r'https?://[^"\']+\.m3u8[^"\']*', html)
    if direct:
        return direct.group(0), channel_url

    return None, None
