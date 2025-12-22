import requests
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def find_active_site(start=1490, end=1600):
    for i in range(start, end):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(site, timeout=5, headers=HEADERS)
            if r.status_code == 200 and "channel.html" in r.text:
                print(f"[OK] Aktif site: {site}")
                return site
        except:
            pass
    return None

def find_baseurl(site):
    url = f"{site}/channel.html?id=yayin1"
    headers = HEADERS.copy()
    headers["Referer"] = site + "/"

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    m = re.search(r'baseurl\\s*[:=]\\s*["\\\']([^"\\\']+)', r.text)
    return m.group(1) if m else None
