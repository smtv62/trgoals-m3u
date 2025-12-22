import requests
from src.cache import load_cached_domain, save_cached_domain

def _is_valid_site(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200 and "channel.html?id=" in r.text
    except requests.RequestException:
        return False

def find_active_site(start=1494, end=1700):
    cached = load_cached_domain()
    if cached and _is_valid_site(cached):
        return cached

    for i in range(start, end):
        url = f"https://trgoals{i}.xyz/"
        if _is_valid_site(url):
            save_cached_domain(url)
            return url
    return None
