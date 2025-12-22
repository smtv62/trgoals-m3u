import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

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

    m3u8 = re.search(r'https?://[^"\']+\.m3u8[^"\']*', html)
    if m3u8:
        return m3u8.group(0)

    return None
