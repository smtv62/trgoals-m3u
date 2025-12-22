import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def resolve_baseurl(site, channel_id):
    url = f"{site}/channel.html?id={channel_id}"

    headers = HEADERS.copy()
    headers["Referer"] = site + "/"

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    html = r.text

    match = re.search(
        r'baseurl\s*[:=]\s*["\']([^"\']+)["\']',
        html
    )

    if match:
        return match.group(1)

    return None
