import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

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

    # view-source analizinden çıkan net pattern
    m = re.search(r'baseurl\s*[:=]\s*["\']([^"\']+)["\']', html)
    if m:
        return m.group(1)

    return None
