import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://trgoals1495.xyz/",
}

def find_baseurl(site):
    url = f"{site}/channel.html?id=yayin1"

    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()

    html = r.text

    match = re.search(
        r'baseurl\s*[:=]\s*["\']([^"\']+)["\']',
        html
    )

    if match:
        return match.group(1)

    return None
