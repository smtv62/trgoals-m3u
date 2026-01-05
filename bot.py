import requests
import re
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def find_active_site():
    for i in range(1495, 1601):
        url = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(url, headers=HEADERS, timeout=5)
            if r.status_code == 200 and "channel" in r.text.lower():
                return url
        except:
            continue
    return None


def clean_channel_name(text: str) -> str:
    """
    Kanal adını normalize eder:
    - Satır sonlarını siler
    - Fazla boşlukları temizler
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_channel_data(active_url):
    channel_map = {}
    base_url_found = None

    r = requests.get(active_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.select("a.channel-item"):
        href = item.get("href", "")
        name_div = item.select_one("div.channel-name")

        if not name_div:
            continue

        id_match = re.search(r'id=([a-zA-Z0-9_]+)', href)
        if not id_match:
            continue

        channel_id = id_match.group(1)
        channel_name = clean_channel_name(name_div.get_text())

        if channel_id and channel_name:
            channel_map[channel_id] = channel_name

    # baseurl yakalama
    test = requests.get(
        f"{active_url}/channel.html?id=yayin1",
        headers=HEADERS,
        timeout=5
    )

    m = re.search(r'const\s+baseurl\s*=\s*"([^"]+)"', test.text)
    if m:
        base_url_found = m.group(1)
    else:
        # fallback
        base_url_found = "https://ogr.d72577a9dd0ec6.sbs/"

    return channel_map, base_url_found


def create_m3u():
    active_site = find_active_site()
    if not active_site:
        print("Aktif site bulunamadı")
        return

    channel_map, base_url = get_channel_data(active_site)
    if not channel_map:
        print("Kanal listesi boş")
        return

    m3u = ["#EXTM3U"]

    for cid, name in channel_map.items():
        stream = f"{base_url}{cid}.m3u8"

        m3u.append(f'#EXTINF:-1,{name}')
        m3u.append(f'#EXTVLCOPT:http-referrer={active_site}/')
        m3u.append(f'#EXTVLCOPT:http-origin={active_site}')
        m3u.append(
            '#EXTVLCOPT:http-user-agent='
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
        m3u.append(stream)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))

    print(f"{len(channel_map)} kanal yazıldı → playlist.m3u")


if __name__ == "__main__":
    create_m3u()
