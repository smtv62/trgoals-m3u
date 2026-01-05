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
        
        # SADECE verdiğin yapıdaki kanal isimlerini süzüyoruz
        # a class="channel-item" içindeki div class="channel-name" metnini alıyoruz
        for item in soup.find_all('a', class_='channel-item'):
            href = item.get('href', '')
            name_div = item.find('div', class_='channel-name')
            
            if 'id=' in href and name_div:
                # İkon metnini (fas fa-tv) değil, sadece kanal ismini al
                channel_name = name_div.get_text(strip=True)
                # id değerini çek (yayin1, yayinb2 vb.)
                channel_id = href.split('id=')[-1]
                
                if channel_name and channel_id:
                    names_and_ids[channel_id] = channel_name

        # Base URL bulma işlemi
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

    m3u_lines = ["#EXTM3U"]
    
    for yid, name in channel_map.items():
        # Dosya adı ve link yapısı
        filename = f"{yid}.m3u8" if not yid.endswith(".m3u8") else yid
        
        m3u_lines.append(f'#EXTINF:-1, {name}')
        # Referer eklemesi
        m3u_lines.append(f'#EXTVLCOPT:http-referrer={active_site}/')
        m3u_lines.append(f'{base_url}{filename}')

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

if __name__ == "__main__":
    create_m3u()
