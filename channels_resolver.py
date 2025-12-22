import requests
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def resolve_channel(site, channel_id):
    channel_url = f"{site}/channel.html?id={channel_id}"

    headers = {
        "User-Agent": UA,
        "Referer": site + "/"
    }

    try:
        r = requests.get(channel_url, headers=headers, timeout=10)
        r.raise_for_status()
    except:
        return None, None

    html = r.text

    # iframe varsa player sayfasını al
    iframe = re.search(r'<iframe[^>]+src=["\']([^"\']+)["\']', html)
    if iframe:
        player_url = iframe.group(1)
        if player_url.startswith("/"):
            player_url = site + player_url

        headers["Referer"] = channel_url

        try:
            pr = requests.get(player_url, headers=headers, timeout=10)
            pr.raise_for_status()
            html = pr.text
        except:
            return None, None

    # gerçek m3u8
    m3u8 = re.search(r'https?://[^"\']+\.m3u8[^"\']*', html)
    if not m3u8:
        return None, None

    return m3u8.group(0), channel_url
