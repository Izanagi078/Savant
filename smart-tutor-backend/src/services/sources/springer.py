import aiohttp
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def search(topic: str, level: str) -> list:
    url = f"https://link.springer.com/search?query={topic.replace(' ', '+')}"
    logger.info(f"🔍 Searching Springer for topic='{topic}'")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning(f"Springer request failed: {resp.status}")
                    return []

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                results = []

                for item in soup.select(".content-item-list .title")[:5]:
                    link_tag = item.select_one("a")
                    if not link_tag:
                        continue
                    title = link_tag.text.strip()
                    link = "https://link.springer.com" + link_tag["href"]
                    results.append({
                        "source": "Springer",
                        "title": title,
                        "description": "",
                        "url": link,
                        "authors": "N/A",
                        "date": "N/A"
                    })

                return results

    except Exception as e:
        logger.exception(f"❌ Springer search error: {e}")
        return []
