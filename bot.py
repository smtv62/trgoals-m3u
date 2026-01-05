import requests
import re
from bs4 import BeautifulSoup

def find_active_site():
    for i in range(1495, 1601):
        url = f"https://trgoals{i}.xyz"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return url
        except:
            continue
    return None

def get_channel_data(active_url):
    names_and_ids = {}
    base_url_found = "https://ogr.d72577a9dd0ec6.sbs/"
    
    try:
        resp = requests.get(active_url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Linkleri ve isimleri tara
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'id=' in href:
                name = link.get_text(strip=True)
                yayin_id = href.split('id=')[-1]
                if name and yayin_id:
                    names_and_ids[yayin_id] = name

        # Base URL bul
        test_page = requests.get(f"{active_url}/channel.html?id=yayin1", timeout=5)
        match = re.search(r'const baseurl = "(https?://[^"]+)"', test_page.text)
        if match:
            base_url_found = match.group(1)
    except:
        pass
    
    return names_and_ids, base_url_found

def create_m3u():
    active_site = find_active_site()
    if not active_site:
        return

    channel_map, base_url = get_channel_data(active_site)
    if not channel_map:
        return

    lines = ["#EXTM3U"]
    
    for yid, name in channel_map.items():
        # Dosya adını belirle (yid zaten yayin1, yayinb2 vs. geliyor)
        # Eğer yid içinde zaten .m3u8 yoksa ekle
        filename = yid if ".m3u8" in yid else f"{yid}.m3u8"
        
        lines.append(f'#EXTINF:-1, {name}')
        lines.append(f'#EXTVLCOPT:http-referrer={active_site}/')
        lines.append(f'{base_url}{filename}')

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    create_m3u()
