import requests
from channels import CHANNELS
from resolver import find_baseurl

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def find_active_site(start=1490, end=1510):
    """
    Aktif siteyi güvenilir biçimde bulur.
    - 200 OK yanıtında içerikte beklenen sinyal (örn. 'channel.html') aranır.
    - Başarısız veya 200 olmayan yanıtlar için diğer adaylara geçer.
    """
    for i in range(start, end + 1):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(site, headers=HEADERS, timeout=5, allow_redirects=False)

            # Yönlendirme durumlarını dikkate almak ister misiniz? Şu anda reddetmiyoruz, sadece logla.
            if r.status_code in (301, 302, 307, 308):
                print(f"[INFO] Yönlendirme: {site} -> {r.headers.get('Location')}")
                continue

            if r.status_code == 200:
                # İçerikte beklenen sinyal (ör. 'channel.html' var mı bak)
                if "channel.html" in r.text or "channels" in r.text or "EXTM3U" in r.text:
                    print(f"[OK] Aktif site bulundu: {site}")
                    return site
                else:
                    print(f"[INFO] 200 ancak içerik güvenilir sinyal içermiyor: {site}")
            else:
                print(f"[INFO] Geçersiz yanıt: {site} - Status {r.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[WARN] İstek hatası {site}: {e}")
            # diğer adaylara geçiş
            continue

    return None

def main():
    site = find_active_site()
    if not site:
        print("[HATA] Aktif site bulunamadı")
        return

    baseurl = find_baseurl(site, "yayin1")
    if not baseurl:
        print("[HATA] BaseURL bulunamadı")
        return

    lines = ["#EXTM3U"]

    for ch in CHANNELS:
        file_path = str(ch.get("file", "")).lstrip("/")
        base = baseurl.rstrip("/")
        stream = f"{base}/{file_path}" if file_path else base

        lines.append(f'#EXTINF:-1,{ch.get("name", "Unknown")}')
        lines.append(f'#EXTVLCOPT:http-referrer={site}/')
        lines.append(stream)

        print(f"[OK] Eklendi: {ch.get('name')}")

    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("[OK] playlist.m3u oluşturuldu")
    except OSError as e:
        print(f"[HATA] playlist yazılamadı: {e}")

if __name__ == "__main__":
    main()
