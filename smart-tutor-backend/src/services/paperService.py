import aiohttp
from bs4 import BeautifulSoup

async def search_arxiv(topic: str, level: str) -> list:
    query = f"{topic}"
    url = f"https://arxiv.org/search/?query={query.replace(' ', '+')}&searchtype=all"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []

            for item in soup.select(".arxiv-result")[:3]:
                title = item.select_one(".title").text.strip()
                link = item.select_one("p.list-title a")["href"]
                desc = item.select_one(".abstract").text.strip()
                results.append({
                    "source": "arXiv",
                    "title": title,
                    "description": desc,
                    "url": link
                })

            return results
