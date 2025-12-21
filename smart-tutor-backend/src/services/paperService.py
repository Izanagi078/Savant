import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, parse_qs, unquote
from typing import List
from src.utils.parserUtils import extract_text_from_pdf
from src.utils.embeddingUtils import get_embedding, cosine_similarity
from src.utils.logger import logger

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def build_duckduckgo_pdf_query(topic: str, context: str) -> str:
    query = f"{topic} {context} review paper filetype:pdf site:.edu OR site:.org OR site:.ac.uk"
    return f"https://html.duckduckgo.com/html/?q={quote(query)}"

def extract_real_pdf_url(href: str) -> str:
    if "duckduckgo.com/l/?" in href and "uddg=" in href:
        parsed = urlparse(href)
        query = parse_qs(parsed.query)
        if "uddg" in query:
            return unquote(query["uddg"][0])
    return href if href.startswith("http") else ""

def fetch_papers_from_duckduckgo(topic: str, context: str, top_k: int = 5) -> List[str]:
    url = build_duckduckgo_pdf_query(topic, context)
    logger.info(f"[PDF] Searching DuckDuckGo for: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"[PDF] Failed to fetch DuckDuckGo results: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        raw_href = a["href"]
        pdf_url = extract_real_pdf_url(raw_href)
        if ".pdf" in pdf_url.lower():
            links.append(pdf_url)
            logger.debug(f"[PDF] Cleaned PDF URL: {pdf_url}")

    logger.info(f"[PDF] Found {len(links)} raw PDF-ish links")

    if not links:
        logger.warning("[PDF] No PDF links found — possibly due to search limitations")
        return []

    pdf_links = list(set(links))
    query_embedding = get_embedding(f"{topic} {context}")
    scored_links = []

    for url in pdf_links:
        try:
            logger.debug(f"[PDF] Scoring: {url}")
            text = extract_text_from_pdf(url)
            if not text:
                logger.debug(f"[PDF] No text extracted from {url}")
                continue
            score = cosine_similarity(query_embedding, get_embedding(text[:1000]))
            logger.debug(f"[PDF] Relevance score: {score:.4f}")
            scored_links.append((url, score))
        except Exception as e:
            logger.error(f"[PDF] Failed to process {url}: {e}")
            continue

    logger.info(f"[PDF] {len(scored_links)} PDFs passed relevance scoring")

    scored_links.sort(key=lambda x: x[1], reverse=True)
    return [url for url, _ in scored_links[:top_k]]
