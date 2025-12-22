import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def get_baseurl(site):
    test_url = f"{site}/channel.html?id=yayin1"

    headers = HEADERS.copy()
    headers["Referer"] = site + "/"

    r = requests.get(test_url, headers=headers, timeout=10)
    r.raise_for_status()

    match = re.search(
        r'baseurl\s*[:=]\s*["\']([^"\']+)["\']',
        r.text
    )

    if not match:
        return None

    return match.group(1)
