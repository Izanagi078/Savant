import aiohttp
from bs4 import BeautifulSoup

async def search_articles(topic: str, level: str) -> list:
    query = f"{level} {topic} tutorial site:geeksforgeeks.org OR site:datacamp.com"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []

            for g in soup.select("div.g")[:3]:
                link = g.select_one("a")["href"]
                title = g.select_one("h3").text if g.select_one("h3") else "Article"
                results.append({
                    "source": "Web",
                    "title": title,
                    "description": f"{topic} article for {level} learners",
                    "url": link
                })

            return results
