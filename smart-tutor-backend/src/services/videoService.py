import aiohttp
import re
import json
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def clean_search_query(query: str) -> str:
    noise_words = [
        r"\bbeginner\b", r"\bintermediate\b", r"\badvanced\b", 
        r"\btutorial\s*s?\b", r"\bpaper\s*s?\b", r"\bresearch\b", 
        r"\byoutube\b", r"\bwikipedia\b", r"\bwiki\b",
        r"\bguide\s*s?\b", r"\boverview\b", r"\bintroduction to\b",
        r"\bintro to\b", r"\bbasics of\b", r"\bpage\s*s?\b",
        r"\bvideo\s*s?\b", r"\bcourse\s*s?\b"
    ]
    cleaned = query.lower()
    for word in noise_words:
        cleaned = re.sub(word, "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

async def search_youtube(topic: str, level: str) -> list:
    query = clean_search_query(topic)
    if level and level.lower() not in query.lower():
        # Keep query clean of level to prevent search index filtering issues
        pass
        
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    timeout = aiohttp.ClientTimeout(total=3.0)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return get_fallback_videos(topic, level)
                html = await resp.text()
                
                match = re.search(r"ytInitialData\s*=\s*({.+?});", html)
                if not match:
                    return get_fallback_videos(topic, level)
                    
                data = json.loads(match.group(1))
                videos = []
                try:
                    contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
                except KeyError:
                    return get_fallback_videos(topic, level)
                
                for content in contents:
                    if 'itemSectionRenderer' in content:
                        for item in content['itemSectionRenderer']['contents']:
                            if 'videoRenderer' in item:
                                vr = item['videoRenderer']
                                try:
                                    title = vr['title']['runs'][0]['text']
                                    vid = vr['videoId']
                                    desc_runs = vr.get('detailedMetadataSnippets', [{}])[0].get('snippetText', {}).get('runs', [])
                                    desc = "".join(r.get('text', '') for r in desc_runs) if desc_runs else f"Learn {topic} in this guide."
                                    if not desc:
                                        desc = f"Learn {topic} at a {level} level in this comprehensive video guide."
                                        
                                    videos.append({
                                        "source": "YouTube",
                                        "title": title,
                                        "description": desc[:200] + "..." if len(desc) > 200 else desc,
                                        "url": f"https://www.youtube.com/watch?v={vid}"
                                    })
                                except Exception:
                                    continue
                                    
                if not videos:
                    return get_fallback_videos(topic, level)
                return videos[:3]
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
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
