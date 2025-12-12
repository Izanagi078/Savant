import aiohttp
from bs4 import BeautifulSoup

async def search_youtube(topic: str, level: str) -> list:
    query = f"{level} {topic} tutorial site:youtube.com"
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []

            for link in soup.select("a[href^='/watch']")[:3]:
                video_url = f"https://www.youtube.com{link['href']}"
                title = link.get("title") or "YouTube Video"
                results.append({
                    "source": "YouTube",
                    "title": title,
                    "description": f"{topic} video for {level} learners",
                    "url": video_url
                })

            return results
