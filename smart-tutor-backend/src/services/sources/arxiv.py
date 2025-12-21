import aiohttp
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def search(topic: str, level: str) -> list:
    url = f"https://arxiv.org/search/?query={topic.replace(' ', '+')}&searchtype=all"
    logger.info(f"🔍 Searching arXiv for topic='{topic}'")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning(f"arXiv request failed: {resp.status}")
                    return []

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                results = []

                for item in soup.select(".arxiv-result")[:5]:
                    title = item.select_one(".title").text.strip()
                    link = item.select_one("p.list-title a")["href"]
                    desc = item.select_one(".abstract").text.strip()
                    authors = item.select_one(".authors").text.strip()
                    date = item.select_one(".is-size-7").text.strip()
                    pdf = link.replace("abs", "pdf")

                    results.append({
                        "source": "arXiv",
                        "title": title,
                        "description": desc,
                        "url": link,
                        "pdf": pdf,
                        "authors": authors,
                        "date": date
                    })

                return results

    except Exception as e:
        logger.exception(f"❌ arXiv search error: {e}")
        return []
