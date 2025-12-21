import aiohttp
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def search(topic: str, level: str) -> list:
    url = f"https://www.mdpi.com/search?q={topic.replace(' ', '+')}"
    logger.info(f"🔍 Searching MDPI for topic='{topic}'")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning(f"MDPI request failed: {resp.status}")
                    return []

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                results = []

                for item in soup.select(".article-content")[:5]:
                    title_tag = item.select_one("h3 a")
                    if not title_tag:
                        continue
                    title = title_tag.text.strip()
                    link = "https://www.mdpi.com" + title_tag["href"]
                    desc = item.select_one(".excerpt").text.strip() if item.select_one(".excerpt") else ""
                    authors = item.select_one(".authors").text.strip() if item.select_one(".authors") else ""

                    results.append({
                        "source": "MDPI",
                        "title": title,
                        "description": desc,
                        "url": link,
                        "authors": authors,
                        "date": "N/A"
                    })

                return results

    except Exception as e:
        logger.exception(f"❌ MDPI search error: {e}")
        return []
