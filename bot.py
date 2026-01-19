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

def find_active_site():
    print("Sistem taranıyor, dolu domain aranıyor...")
    for i in range(1495, 1601):
        url = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(url, headers=HEADERS, timeout=3, verify=False, allow_redirects=True)
            if r.status_code == 200:
                # Sadece domainin açık olması yetmez, içinde kanal listesi var mı bakıyoruz
                if "channel-item" in r.text:
                    final_url = r.url.rstrip('/')
                    print(f"[+] Aktif ve dolu domain: {final_url}")
                    return final_url
        except:
            continue
    return None

def get_channel_data(active_url):
    channel_map = {}
    base_url_found = None # Yedek adresi sildik!

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

        # 2. Dinamik Kaynak Avı (Derin Tarama)
        # Sitenin içindeki TÜM script dosyalarını bul
        scripts = soup.find_all("script", src=True)
        potential_sources = [f"{active_url}/channel.html?id=yayin1", active_url]
        
        # Önce HTML içindeki script dosyalarının adreslerini listeye ekle
        for s in scripts:
            script_url = s['src']
            if not script_url.startswith('http'):
                script_url = f"{active_url}/{script_url.lstrip('/')}"
            potential_sources.append(script_url)

        print(f"Kaynak aranıyor ({len(potential_sources)} farklı nokta taranacak)...")

        for source in potential_sources:
            try:
                res = requests.get(source, headers=HEADERS, timeout=5, verify=False)
                # Regex: .sbs/ ile biten tırnak içindeki her şeyi ara
                matches = re.findall(r'https?://[a-zA-Z0-9.-]+\.sbs/', res.text)
                if matches:
                    base_url_found = matches[0]
                    print(f"[!] Yayın kaynağı başarıyla yakalandı: {base_url_found}")
                    break
            except:
                continue

    except Exception as e:
        print(f"[-] Hata: {e}")

    return channel_map, base_url_found

def create_m3u():
    active_site = find_active_site()
    if not active_site:
        print("[-] HATA: Aktif bir TRGoals domaini bulunamadı!")
        return

    channels, base_url = get_channel_data(active_site)
    
    if not base_url:
        print("[-] HATA: Yayın kaynağı (baseurl) otomatik olarak yakalanamadı!")
        print("Sitenin kod yapısı değişmiş olabilir.")
        return

    if not channels:
        print("[-] HATA: Kanal listesi çekilemedi!")
        return

    m3u = ["#EXTM3U"]
    for cid, name in channels.items():
        m3u.append(f'#EXTINF:-1 group-title="TRGoals",{name}')
        m3u.append(f'#EXTVLCOPT:http-referrer={active_site}/')
        m3u.append(f'#EXTVLCOPT:http-user-agent={HEADERS["User-Agent"]}')
        m3u.append(f"{base_url}{cid}.m3u8")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u))

    print(f"\n--- BAŞARILI ---")
    print(f"Domain: {active_site}")
    print(f"Kaynak: {base_url}")
    print(f"Kanal: {len(channels)}")

if __name__ == "__main__":
    create_m3u()
