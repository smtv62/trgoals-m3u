import requests
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

NEONSPOR_URL = "https://raw.githubusercontent.com/primatzeka/kurbaga/main/NeonSpor/NeonSpor.m3u"

def find_active_site():
    print("Aktif TRGoals taranıyor...")
    for i in range(1495, 1601):
        url = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(url, headers=HEADERS, timeout=4, verify=False)
            if r.status_code == 200:
                return url
        except:
            continue
    return None

def get_channel_data(active_url):
    channel_map = {}
    base_url_found = None

    try:
        # 1. Kanalları Çek
        r = requests.get(active_url, headers=HEADERS, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.select("a.channel-item"):
            href = item.get("href", "")
            name_div = item.select_one("div.channel-name")
            id_match = re.search(r"id=([a-zA-Z0-9_]+)", href)
            if id_match and name_div:
                channel_map[id_match.group(1)] = name_div.get_text().strip()

        # 2. Dinamik Yayın Kaynağını (Base URL) Bul
        # Önce yayin1 sayfasına gidiyoruz
        test_url = f"{active_url}/channel.html?id=yayin1"
        test_res = requests.get(test_url, headers=HEADERS, timeout=10, verify=False)
        
        # Regex Avcısı: İçinde .sbs geçen ve tırnak içinde olan URL yapılarını ara
        # Bu pattern https://f7r.d72577a9dd0ec10.sbs/ gibi yapıları yakalar
        patterns = [
            r'https?://[a-z0-9]+\.[a-z0-9]+\.sbs/', 
            r'const\s+baseurl\s*=\s*"([^"]+)"',
            r'var\s+src\s*=\s*"([^"]+)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, test_res.text)
            if match:
                # Eğer ilk pattern (genel URL) yakalarsa grubu değil tamamını al
                found = match.group(1) if "(" in pattern else match.group(0)
                if ".sbs" in found:
                    base_url_found = found
                    break
        
        # Hala bulunamadıysa manuel verdiğin güncel adresi yedek yapalım
        if not base_url_found:
            base_url_found = "https://f7r.d72577a9dd0ec10.sbs/"
            print("(!) Otomatik kaynak bulunamadı, manuel yedek kullanılıyor.")

    except Exception as e:
        print(f"Hata: {e}")
        base_url_found = "https://f7r.d72577a9dd0ec10.sbs/"

    return channel_map, base_url_found

def fetch_neonspor():
    try:
        r = requests.get(NEONSPOR_URL, timeout=10)
        lines = []
        for line in r.text.splitlines():
            if line.startswith("#EXTINF"):
                if 'group-title=' not in line:
                    line = line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="NeonSpor"')
            if not line.startswith("#EXTM3U"):
                lines.append(line)
        return lines
    except:
        return []

def create_m3u():
    active_site = find_active_site()
    if not active_site:
        print("Aktif site bulunamadı.")
        return

    channel_map, base_url = get_channel_data(active_site)
    print(f"Kullanılan Yayın Kaynağı: {base_url}")

    m3u = ["#EXTM3U"]
    for cid, name in channel_map.items():
        stream = f"{base_url}{cid}.m3u8"
        m3u.append(f'#EXTINF:-1 group-title="TRGoals",{name}')
        m3u.append(f'#EXTVLCOPT:http-referrer={active_site}/')
        m3u.append(f'#EXTVLCOPT:http-origin={active_site}')
        m3u.append(f'#EXTVLCOPT:http-user-agent={HEADERS["User-Agent"]}')
        m3u.append(stream)

    m3u.extend(fetch_neonspor())

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))

    print(f"playlist.m3u oluşturuldu. ({len(channel_map)} kanal)")

if __name__ == "__main__":
    create_m3u()
