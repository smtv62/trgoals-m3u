import re, requests

PATTERN = re.compile(r'https?://[^"\']+/yayinzirve\.m3u8', re.I)

def find_base_url(channel_url):
    try:
        r = requests.get(channel_url, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return None

    m = PATTERN.search(r.text)
    if not m:
        return None
    return m.group(0).rsplit("/", 1)[0] + "/"
