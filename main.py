import requests
import re
import sys

KANALLAR = [
    {"id": "yayin1", "tvg_id": "BeinSports1.tr", "kanal_adi": "Bein Sports 1 HD"},
    {"id": "yayinb2", "tvg_id": "BeinSports2.tr", "kanal_adi": "Bein Sports 2 HD"},
    {"id": "yayinb3", "tvg_id": "BeinSports3.tr", "kanal_adi": "Bein Sports 3 HD"},
    # diğer kanallar buraya...
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def find_active_site(start=1495, end=1700):
    for i in range(start, end+1):
        url = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(url, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                return url
        except requests.RequestException:
            continue
    return None

def resolve_channel(site, channel_id):
    channel_url = f"{site}/channel.html?id={channel_id}"
    headers = HEADERS.copy()
    headers["Referer"] = site + "/"

    try:
        r = requests.get(channel_url, headers=headers, timeout=10)
        r.raise_for_status()
    except:
        return None

    html = r.text

    # iframe içinden m3u8 arama
    iframe = re.search(r'iframe[^>]+src=["\']([^"\']+)["\']', html)
    if iframe:
        player_url = iframe.group(1)
        if player_url.startswith("/"):
            player_url = site + player_url
        headers["Referer"] = channel_url
        try:
            pr = requests.get(player_url, headers=headers, timeout=10)
            pr.raise_for_status()
        except:
            return None
        m3u8 = re.search(r'https?://[^"\']+\.m3u8[^"\']*', pr.text)
        if m3u8:
            return m3u8.group(0)

    # fallback: direkt html içinde m3u8
    m3u8 = re.search(r'https?://[^"\']+\.m3u8[^"\']*', html)
    if m3u8:
        return m3u8.group(0)

    return None

def generate_playlist(site):
    lines = ["#EXTM3U"]
    active = False
    for ch in KANALLAR:
        stream = resolve_channel(site, ch["id"])
        if stream:
            active = True
            lines.append(f'#EXTINF:-1 tvg-id="{ch["tvg_id"]}",{ch["kanal_adi"]}')
            lines.append(f'#EXTVLCOPT:http-user-agent={HEADERS["User-Agent"]}')
            lines.append(f'#EXTVLCOPT:http-referrer={site}/')
            lines.append(stream)
            print(f"[OK] Çözüldü: {ch['kanal_adi']}")
        else:
            print(f"[!] Çözülmedi: {ch['kanal_adi']}")
    return "\n".join(lines), active

def main():
    site = find_active_site()
    if not site:
        print("[HATA] Aktif site bulunamadı.")
        sys.exit(1)
    print(f"[OK] Aktif site: {site}")

    playlist, active = generate_playlist(site)
    if not active:
        print("Playlist boş, çıkılıyor.")
        sys.exit(1)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)
    print("Playlist oluşturuldu: playlist.m3u")

if __name__ == "__main__":
    main()
