from channels import CHANNELS

SITE = "https://trgoals1494.xyz"

lines = ["#EXTM3U"]

for ch in CHANNELS:
    stream_url = f"{SITE}/{ch['id']}.m3u8"

    lines.append(f"#EXTINF:-1,{ch['name']}")
    lines.append(f"#EXTVLCOPT:http-referrer={SITE}/")
    lines.append(f"#EXTVLCOPT:http-user-agent=Mozilla/5.0")
    lines.append(stream_url)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("[OK] playlist.m3u oluşturuldu")
