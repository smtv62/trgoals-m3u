from src.channels import KANALLAR

def generate_m3u(base_url, referer, user_agent="Mozilla/5.0"):
    lines = ["#EXTM3U"]
    for k in KANALLAR:
        name = f"ÜmitM0d {k['kanal_adi']}"
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{name}",{name}')
        lines.append(f"#EXTVLCOPT:http-user-agent={user_agent}")
        lines.append(f"#EXTVLCOPT:http-referrer={referer}")
        lines.append(base_url + k["dosya"])
    return "\n".join(lines)
