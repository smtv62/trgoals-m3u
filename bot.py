import requests
import re
import os

def find_active_site():
    for i in range(1495, 1601):
        url = f"https://trgoals{i}.xyz"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"Aktif site bulundu: {url}")
                return url
        except:
            continue
    return None

def get_base_url(active_url):
    # Örnek olarak yayin1 üzerinden base_url çekiyoruz
    test_url = f"{active_url}/channel.html?id=yayin1"
    try:
        resp = requests.get(test_url, timeout=5)
        # Regex ile baseurl değişkenini yakalıyoruz
        match = re.search(r'const baseurl = "(https?://[^"]+)"', resp.text)
        if match:
            return match.group(1)
    except:
        pass
    return "https://ogr.d72577a9dd0ec6.sbs/" # Fallback

def create_m3u():
    active_site = find_active_site()
    if not active_site:
        print("Aktif site bulunamadı.")
        return

    base_url = get_base_url(active_site)
    
    kanallar = {
        1: "yayin1.m3u8", 2: "yayinb2.m3u8", 3: "yayinb3.m3u8", 4: "yayinb4.m3u8",
        5: "yayinb5.m3u8", 6: "yayinbm1.m3u8", 7: "yayinbm2.m3u8", 8: "yayinss.m3u8",
        9: "yayinss2.m3u8", 10: "yayinssp2.m3u8", 11: "yayint1.m3u8", 12: "yayint2.m3u8",
        13: "yayint3.m3u8", 14: "yayinsmarts.m3u8", 15: "yayinsms2.m3u8", 16: "yayintrtspor.m3u8",
        17: "yayintrtspor2.m3u8", 18: "yayinas.m3u8", 19: "yayinatv.m3u8", 20: "yayintv8.m3u8",
        21: "yayintv85.m3u8", 22: "yayinnbatv.m3u8", 23: "yayinex1.m3u8", 24: "yayinex2.m3u8",
        25: "yayinex3.m3u8", 26: "yayinex4.m3u8", 27: "yayinex5.m3u8", 28: "yayinex6.m3u8",
        29: "yayinex7.m3u8", 30: "yayinex8.m3u8"
    }

    m3u_content = "#EXTM3U\n"
    
    for ch_id, ch_file in kanallar.items():
        # Referer eklenmiş haliyle formatlıyoruz
        line = f'#EXTINF:-1, Kanal {ch_id}\n'
        line += f'#EXTVLCOPT:http-referrer={active_site}/\n'
        line += f'{base_url}{ch_file}\n'
        m3u_content += line

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Playlist güncellendi.")

if __name__ == "__main__":
    create_m3u()
