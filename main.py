from channels import CHANNELS
from resolver import resolve_channel

OUTPUT_FILE = "playlist.m3u"
USER_AGENT = "Mozilla/5.0"

def main():
    site = find_active_site()
    if not site:
        print("Aktif site bulunamadı.")
        return

    print(f"[OK] Aktif site bulundu: {site}")

    lines = ["#EXTM3U"]
    success = 0

    for ch in CHANNELS:
        stream = resolve_channel(site, ch["id"])
        if not stream:
            print(f"[!] Çözülmedi: {ch['name']}")
            continue

        lines.append(
            f'#EXTINF:-1 tvg-id="{ch["tvg_id"]}",{ch["name"]}'
        )
        lines.append(f'#EXTVLCOPT:http-user-agent={USER_AGENT}')
        lines.append(f'#EXTVLCOPT:http-referrer={site}/channel.html?id={ch["id"]}')
        lines.append(stream)

        success += 1
        print(f"[OK] Çözüldü: {ch['name']}")

    if success == 0:
        print("Playlist boş, çıkılıyor.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Playlist oluşturuldu → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
