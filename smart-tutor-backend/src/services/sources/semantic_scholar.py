import aiohttp
import logging

logger = logging.getLogger(__name__)

async def search(topic: str, level: str) -> list:
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={topic}&limit=5&fields=title,abstract,url,authors,year"
    logger.info(f"🔍 Searching Semantic Scholar for topic='{topic}'")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.warning(f"Semantic Scholar request failed: {resp.status}")
                    return []

                data = await resp.json()
                return [{
                    "source": "Semantic Scholar",
                    "title": p["title"],
                    "description": p.get("abstract", ""),
                    "url": p["url"],
                    "authors": ", ".join(a["name"] for a in p.get("authors", [])),
                    "date": p.get("year", "N/A")
                } for p in data.get("data", [])]

    except Exception as e:
        logger.exception(f"❌ Semantic Scholar search error: {e}")
        return []
