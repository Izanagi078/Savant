import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, parse_qs, unquote
from src.utils.logger import logger

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def build_query_url(topic: str, context: str, page: int = 0) -> str:
    query = f"{topic} {context} review paper filetype:pdf site:.edu OR site:.org OR site:.ac.uk"
    return f"https://html.duckduckgo.com/html/?q={quote(query)}&s={page * 30}"

def extract_real_pdf_url(href: str) -> str:
    if "duckduckgo.com/l/?" in href and "uddg=" in href:
        parsed = urlparse(href)
        query = parse_qs(parsed.query)
        if "uddg" in query:
            return unquote(query["uddg"][0])
    return href if href.startswith("http") else ""

def fetch_pdf_links(topic: str, context: str, min_links: int = 10, max_pages: int = 3) -> list:
    collected = set()
    for page in range(max_pages):
        url = build_query_url(topic, context, page)
        logger.info(f"[PDF] Searching DuckDuckGo page {page+1}: {url}")
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
        except Exception as e:
            logger.error(f"[PDF] Failed to fetch page {page+1}: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        for a in soup.find_all("a", href=True):
            raw_href = a["href"]
            pdf_url = extract_real_pdf_url(raw_href)
            if ".pdf" in pdf_url.lower():
                logger.debug(f"[PDF] Cleaned PDF URL: {pdf_url}")
                collected.add(pdf_url)

        if len(collected) >= min_links:
            break

    logger.info(f"[PDF] Collected {len(collected)} unique PDF links")
    return list(collected)
