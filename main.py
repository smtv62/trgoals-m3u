import requests
import re
import logging
from channels import CHANNELS
from resolver import find_baseurl

# Logging ayarları
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def find_active_site(start=1495, end=1700):
    """
    Aktif siteyi bulmaya çalışır.
    - Yönlendirme durumlarını loglar ve atlar.
    - 2xx yanıtlarında içerikte kendi domain adını arar.
    - BaseURL testi için find_baseurl kullanır.
    """
    for i in range(start, end + 1):
        site = f"https://trgoals{i}.xyz"
        try:
            r = requests.get(
                site,
                headers=HEADERS,
                timeout=6,
                allow_redirects=False
            )

            # Yönlendirme durumlarını logla ve ilerle
            if r.status_code in (301, 302, 307, 308):
                logging.info(f"Yönlendirme ({r.status_code}) atlandı: {site} -> {r.headers.get('Location')}")
                continue

            # 2xx yanıtlarını değerlendir
            if 200 <= r.status_code < 300:
                if f"trgoals{i}.xyz" in r.text:
                    test_base = find_baseurl(site, "yayin1")
                    if test_base:
                        logging.info(f"[OK] Aktif site bulundu: {site}")
                        return site
                    else:
                        logging.info(f"[INFO] BaseURL bulunamadı -> {site} reddedildi")
                else:
                    logging.info(f"[INFO] İçerikte alan adı bulunamadı: {site}")
            else:
                logging.info(f"[INFO] Geçersiz yanıt: {site} - Status {r.status_code}")

        except requests.exceptions.RequestException as e:
            logging.warning(f"[HATA] İstek hatası {site}: {e}")
            continue
        except Exception as e:
            logging.warning(f"[HATA] Beklenmedik hata {site}: {e}")
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
        # file yolunda hataya yol açmamak için normalize et
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
