import requests
import re
import urllib3
from bs4 import BeautifulSoup

# SSL uyarılarını sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

NEONSPOR_URL = "https://raw.githubusercontent.com/primatzeka/kurbaga/main/NeonSpor/NeonSpor.m3u"

def find_active_site():
    print("Sistem taranıyor, dolu domain aranıyor...")
    for i in range(1495, 1601):
        url = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(url, headers=HEADERS, timeout=3, verify=False, allow_redirects=True)
            if r.status_code == 200:
                if "channel-item" in r.text:
                    final_url = r.url.rstrip('/')
                    print(f"[+] Aktif ve dolu domain: {final_url}")
                    return final_url
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
        items = soup.select("a.channel-item")
        
        for item in items:
            href = item.get("href", "")
            name_div = item.select_one("div.channel-name")
            cid = re.search(r"id=([a-zA-Z0-9_]+)", href)
            if cid and name_div:
                channel_map[cid.group(1)] = name_div.get_text().strip()

        # 2. Derin Script Taraması
        scripts = soup.find_all("script", src=True)
        potential_sources = [f"{active_url}/channel.html?id=yayin1", active_url]
        for s in scripts:
            script_url = s['src']
            if not script_url.startswith('http'):
                script_url = f"{active_url}/{script_url.lstrip('/')}"
            potential_sources.append(script_url)

        for source in potential_sources:
            try:
                res = requests.get(source, headers=HEADERS, timeout=5, verify=False)
                matches = re.findall(r'https?://[a-zA-Z0-9.-]+\.sbs/', res.text)
                if matches:
                    base_url_found = matches[0]
                    break
            except:
                continue
    except Exception as e:
        print(f"[-] Hata: {e}")

    return channel_map, base_url_found

def fetch_neonspor():
    """NeonSpor M3U listesini çeker ve group-title ekler"""
    print("NeonSpor listesi çekiliyor...")
    try:
        r = requests.get(NEONSPOR_URL, timeout=10)
        lines = []
        for line in r.text.splitlines():
            if line.startswith("#EXTINF"):
                if 'group-title=' not in line:
                    line = line.replace("#EXTINF:-1", '#EXTINF:-1 group-title="NeonSpor"')
            if not line.startswith("#EXTM3U") and line.strip():
                lines.append(line)
        return lines
    except:
        print("[-] NeonSpor listesi alınamadı!")
        return []

def create_m3u():
    active_site = find_active_site()
    if not active_site:
        print("[-] HATA: Aktif bir TRGoals domaini bulunamadı!")
        return

    channels, base_url = get_channel_data(active_site)
    
    if not base_url:
        print("[-] HATA: Yayın kaynağı (baseurl) otomatik yakalanamadı!")
        return

    m3u = ["#EXTM3U"]

    # ---------- TRGOALS EKLEME ----------
    print(f"TRGoals kanalları ekleniyor ({len(channels)} adet)...")
    for cid, name in channels.items():
        m3u.append(f'#EXTINF:-1 group-title="TRGoals",{name}')
        m3u.append(f'#EXTVLCOPT:http-referrer={active_site}/')
        m3u.append(f'#EXTVLCOPT:http-user-agent={HEADERS["User-Agent"]}')
        m3u.append(f"{base_url}{cid}.m3u8")

    # ---------- NEONSPOR EKLEME ----------
    neon_lines = fetch_neonspor()
    if neon_lines:
        m3u.extend(neon_lines)
        print(f"NeonSpor kanalları eklendi ✔")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))

    print(f"\n--- İŞLEM TAMAM ---")
    print(f"Playlist hazır! Toplam TRGoals: {len(channels)}")

if __name__ == "__main__":
    create_m3u()
