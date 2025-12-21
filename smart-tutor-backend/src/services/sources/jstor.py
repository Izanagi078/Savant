import aiohttp
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def search(topic: str, level: str) -> list:
    url = f"https://www.jstor.org/action/doBasicSearch?Query={topic.replace(' ', '+')}"
    logger.info(f"🔍 Searching JSTOR for topic='{topic}'")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning(f"JSTOR request failed: {resp.status}")
                    return []

                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                results = []

                for item in soup.select(".search-result")[:5]:
                    title_tag = item.select_one(".title a")
                    if not title_tag:
                        continue
                    title = title_tag.text.strip()
                    link = "https://www.jstor.org" + title_tag["href"]
                    desc = item.select_one(".snippet").text.strip() if item.select_one(".snippet") else ""

                    results.append({
                        "source": "JSTOR",
                        "title": title,
                        "description": desc,
                        "url": link,
                        "authors": "N/A",
                        "date": "N/A"
                    })

                return results

    except Exception as e:
        logger.exception(f"❌ JSTOR search error: {e}")
        return []
