from pathlib import Path

CACHE_FILE = Path(".last_domain")

def load_cached_domain():
    return CACHE_FILE.read_text().strip() if CACHE_FILE.exists() else None

def save_cached_domain(domain):
    CACHE_FILE.write_text(domain)
