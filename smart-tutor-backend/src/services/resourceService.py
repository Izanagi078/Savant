import aiohttp
import re
import urllib.parse
from bs4 import BeautifulSoup
from src.services.videoService import clean_search_query

async def search_articles(topic: str, level: str) -> list:
    cleaned = clean_search_query(topic)
    if not cleaned:
        cleaned = topic
        
    results = []
    seen_urls = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        # 1. Wikipedia Search
        try:
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={cleaned.replace(' ', '+')}&limit=3&namespace=0&format=json"
            async with session.get(wiki_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if len(data) >= 4:
                        titles = data[1]
                        descriptions = data[2]
                        links = data[3]
                        
                        for i in range(len(titles)):
                            title = titles[i]
                            desc = descriptions[i] if descriptions[i] else f"Reference article on {title}."
                            link = links[i]
                            if link not in seen_urls:
                                results.append({
                                    "source": "Wikipedia",
                                    "title": title,
                                    "description": desc[:200] + "..." if len(desc) > 200 else desc,
                                    "url": link
                                })
                                seen_urls.add(link)
        except Exception:
            pass

        # 2. General Web Search (DuckDuckGo HTML)
        try:
            ddg_url = f"https://html.duckduckgo.com/html/?q={cleaned.replace(' ', '+')}"
            async with session.get(ddg_url) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    
                    for a in soup.find_all("a", class_="result__a"):
                        title = a.text.strip()
                        link = a["href"]
                        
                        if "uddg=" in link:
                            match = re.search(r"uddg=(.+?)(&|$)", link)
                            if match:
                                link = urllib.parse.unquote(match.group(1))
                                
                        if any(domain in link for domain in ["duckduckgo.com", "google.com", "bing.com", "trip.com"]):
                            continue
                            
                        if link not in seen_urls:
                            # Try to extract the snippet text
                            parent_div = a.find_parent("div", class_="result__body")
                            desc = "No description available."
                            if parent_div:
                                snippet_elem = parent_div.find("a", class_="result__snippet")
                                if snippet_elem:
                                    desc = snippet_elem.text.strip()
                            if not desc or desc == "No description available.":
                                desc = f"Discover online tutorials, study guides, and articles about {cleaned}."
                                
                            results.append({
                                "source": "Web",
                                "title": title,
                                "description": desc[:200] + "..." if len(desc) > 200 else desc,
                                "url": link
                            })
                            seen_urls.add(link)
                            if len(results) >= 5:
                                break
        except Exception:
            pass

    if not results:
        return get_fallback_articles(topic, level)
        
    return results[:3]

def get_fallback_articles(topic: str, level: str) -> list:
    cleaned = clean_search_query(topic)
    if not cleaned:
        cleaned = topic
    return [
        {
            "source": "Wikipedia",
            "title": f"Introduction to {cleaned.title()}",
            "description": f"A comprehensive introduction and reference manual to understand {cleaned} core paradigms.",
            "url": f"https://en.wikipedia.org/wiki/{cleaned.replace(' ', '_').capitalize()}"
        },
        {
            "source": "Web",
            "title": f"Best Practices for {cleaned.title()} Learning",
            "description": f"Guidelines and industry standards to streamline your learning curve in {cleaned}.",
            "url": "https://geeksforgeeks.org"
        }
    ]
