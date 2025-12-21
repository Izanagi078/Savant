import requests
from src.utils.logger import logger

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def is_valid_pdf_url(url: str) -> bool:
    try:
        head = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=5)
        content_type = head.headers.get("Content-Type", "")
        return "application/pdf" in content_type.lower()
    except Exception as e:
        logger.debug(f"[PDF] HEAD request failed for {url}: {e}")
        return False
