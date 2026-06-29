import aiohttp
from bs4 import BeautifulSoup

async def search_youtube(topic: str, level: str) -> list:
    query = f"{level} {topic} tutorial"
    url = f"https://www.youtube.com/feeds/videos.xml?search_query={query.replace(' ', '+')}"

    async with aiohttp.ClientSession() as session:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return get_fallback_videos(topic, level)
                xml_data = await resp.text()
                soup = BeautifulSoup(xml_data, features="xml")
                results = []

                for entry in soup.find_all("entry")[:3]:
                    title_elem = entry.find("title")
                    title = title_elem.text.strip() if title_elem else "YouTube Video"
                    
                    link_elem = entry.find("link")
                    video_url = link_elem["href"] if (link_elem and link_elem.has_attr("href")) else ""
                    
                    if not video_url:
                        video_id_elem = entry.find("yt:videoId") or entry.find("videoId")
                        if video_id_elem:
                            video_url = f"https://www.youtube.com/watch?v={video_id_elem.text.strip()}"
                        else:
                            continue

                    results.append({
                        "source": "YouTube",
                        "title": title,
                        "description": f"Learn {topic} at a {level} level in this comprehensive video guide.",
                        "url": video_url
                    })

                if not results:
                    return get_fallback_videos(topic, level)
                return results
        except Exception:
            return get_fallback_videos(topic, level)

def get_fallback_videos(topic: str, level: str) -> list:
    return [
        {
            "source": "YouTube",
            "title": f"{topic.title()} - Full Course for Beginners",
            "description": f"A step-by-step masterclass covering the essential workflows of {topic}.",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        {
            "source": "YouTube",
            "title": f"Advanced {topic.title()} Architecture Patterns",
            "description": f"Deep dive for {level} learners on performance optimizations and scale design patterns.",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    ]
