import requests
import re
import sys

KANALLAR = [
    {"dosya": "yayin1", "tvg_id": "BeinSports1.tr", "kanal_adi": "Bein Sports 1 HD"},
    {"dosya": "yayinb2", "tvg_id": "BeinSports2.tr", "kanal_adi": "Bein Sports 2 HD"},
    {"dosya": "yayinb3", "tvg_id": "BeinSports3.tr", "kanal_adi": "Bein Sports 3 HD"},
    {"dosya": "yayinb4", "tvg_id": "BeinSports4.tr", "kanal_adi": "Bein Sports 4 HD"},
    {"dosya": "yayinb5", "tvg_id": "BeinSports5.tr", "kanal_adi": "Bein Sports 5 HD"},
    {"dosya": "yayinss", "tvg_id": "SSport1.tr", "kanal_adi": "S Sport HD"},
    {"dosya": "yayintrtspor", "tvg_id": "TRTSpor.tr", "kanal_adi": "TRT Spor HD"},
    {"dosya": "yayinas", "tvg_id": "ASpor.tr", "kanal_adi": "A Spor HD"},
    {"dosya": "yayinatv", "tvg_id": "ATV.tr", "kanal_adi": "ATV HD"},
    {"dosya": "yayintv8", "tvg_id": "TV8.tr", "kanal_adi": "TV8 HD"},
]

USER_AGENT = "Mozilla/5.0"

def find_active_site():
    for i in range(1494, 1700):
        url = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200 and "channel.html?id=" in r.text:
                print(f"[OK] Aktif site bulundu: {url}")
                return url
        except:
            continue
    return None

def resolve_stream(site, channel_id):
    url = f"{site}/channel.html?id={channel_id}"
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": site + "/"
    }

    r = requests.get(url, headers=headers, timeout=10)

    # iframe içinden m3u8 çek
    iframe_match = re.search(r'src="([^"]+\.m3u8[^"]*)"', r.text)
    if iframe_match:
        return iframe_match.group(1)

    # JS içinden m3u8 çek
    js_match = re.search(r'(https?://[^"\']+\.m3u8[^"\']*)', r.text)
    if js_match:
        return js_match.group(1)

    return None

def generate_playlist(site):
    lines = ["#EXTM3U"]

    for ch in KANALLAR:
        stream = resolve_stream(site, ch["dosya"])
        if not stream:
            print(f"[!] Çözülmedi: {ch['kanal_adi']}")
            continue

        lines.append(
            f'#EXTINF:-1 tvg-id="{ch["tvg_id"]}" tvg-name="{ch["kanal_adi"]}",{ch["kanal_adi"]}'
        )
        lines.append(f'#EXTVLCOPT:http-user-agent={USER_AGENT}')
        lines.append(f'#EXTVLCOPT:http-referrer={site}/')
        lines.append(stream)

        print(f"[✓] Eklendi: {ch['kanal_adi']}")

    return "\n".join(lines)

def main():
    site = find_active_site()
    if not site:
        print("Aktif site bulunamadı.")
        sys.exit(1)

    playlist = generate_playlist(site)

    if playlist.strip() == "#EXTM3U":
        print("Playlist boş, çıkılıyor.")
        sys.exit(1)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print("\n[OK] playlist.m3u oluşturuldu")

if __name__ == "__main__":
    main()
