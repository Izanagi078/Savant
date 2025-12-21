import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from typing import List, Dict
from src.utils.logger import logger

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def build_duckduckgo_url(topic: str, level: str, context: str = "") -> str:
    query = f"educational articles about {topic} {context} for {level} learners".strip()
    return f"https://html.duckduckgo.com/html/?q={quote(query)}"

def fetch_articles(topic: str, level: str, context: str = "") -> List[Dict]:
    url = build_duckduckgo_url(topic, level, context)
    logger.info(f"Fetching articles for topic: {topic}, level: {level}, context: {context}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch search results: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.find_all("a", class_="result__a", limit=15):
        title = result.get_text()
        href = result.get("href")
        snippet_tag = result.find_parent("div", class_="result").find("a", class_="result__snippet")
        snippet = snippet_tag.get_text() if snippet_tag else ""

        if href and title:
            results.append({
                "title": title.strip(),
                "url": href.strip(),
                "snippet": snippet.strip()
            })

    logger.info(f"Fetched {len(results)} raw articles")
    return results

