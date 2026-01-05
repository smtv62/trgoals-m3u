import requests
import re
from bs4 import BeautifulSoup

def find_active_site():
    for i in range(1495, 1601):
        url = f"https://trgoals{i}.xyz"
        try:
            # Sitenin gerçekten orada olup olmadığını kontrol et
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return url
        except:
            continue
    return None

def get_channel_data(active_url):
    names_and_ids = {}
    base_url_found = "https://ogr.d72577a9dd0ec6.sbs/" # Default
    
    try:
        resp = requests.get(active_url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Sitedeki tüm <a> etiketlerini tara
        # href içinde 'id=yayin' geçenleri bul ve isimlerini al
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'id=yayin' in href:
                # Linkin içindeki metni temizle (Kanal İsmi)
                name = link.get_text(strip=True)
                # href'den ID kısmını al (yayin1, yayinb2 vb.)
                yayin_id = href.split('id=')[-1]
                
                if name and yayin_id:
                    names_and_ids[yayin_id] = name

        # Base URL bulma (Hangi kanal sayfası olursa olsun aynı script içindedir)
        test_page = requests.get(f"{active_url}/channel.html?id=yayin1", timeout=5)
        match = re.search(r'const baseurl = "(https?://[^"]+)"', test_page.text)
        if match:
            base_url_found = match.group(1)

    except Exception as e:
        print(f"Veri çekilirken hata oluştu: {e}")
    
    return names_and_ids, base_url_found

def create_m3u():
    active_site = find_active_site()
    if not active_site:
        print("Aktif site bulunamadı.")
        return

    print(f"Aktif site: {active_site}")
    channel_map, base_url = get_channel_data(active_site)
    
    # Senin verdiğin sabit liste (Eğer siteden isim çekilemezse yedek olarak kullanılabilir)
    fallback_kanallar = {
        "yayin1": "yayin1.m3u8", "yayinb2": "yayinb2.m3u8", "yayinb3": "yayinb3.m3u8",
        # ... (Diğerleri)
    }

    m3u_content = "#EXTM3U\n"
    
    # Siteden çekilen kanalları dön
    for yid, name in channel_map.items():
        # m3u8 uzantısını ekle (id 'yayin1' ise dosya 'yayin1.m3u8' oluyor)
        filename = f"{yid}.m3u8"
        
        m3u_content += f'#EXTINF:-1, {name}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer={active_
