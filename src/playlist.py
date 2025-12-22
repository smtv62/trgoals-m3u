# src/playlist.py
from src.channels import CHANNELS
from src.channel_resolver import resolve_from_channel

def generate_m3u(site):
    lines = ["#EXTM3U"]

    for ch in CHANNELS:
        print(f"🔍 {ch['kanal_adi']} çözülüyor...")
        stream = resolve_from_channel(site, ch["id"])

        if not stream:
            print("  ❌ bulunamadı")
            continue

        print("  ✅ OK")
        lines.append(f'#EXTINF:-1,{ch["kanal_adi"]}')
        lines.append(stream)

    return "\n".join(lines)
