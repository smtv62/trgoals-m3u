# src/channel_resolver.py

def resolve_from_channel(site, channel_id):
    # HTML'den net olarak çıktı:
    baseurl = "https://ig9.d72577a9dd0ec5.sbs/"
    return baseurl + channel_id + ".m3u8"
