import os
import aiohttp
import logging

# Configure logger
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
from pathlib import Path

# Load .env from two levels up
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

async def search_youtube(topic: str, level: str, context: str = "") -> list:
    if not YOUTUBE_API_KEY:
        logger.warning("⚠️ No YouTube API key found. Skipping video search.")
        return []

    # Combine topic, level, and context into the search query
    query = f"{level} {topic} {context} tutorial".strip()
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 3,
        "key": YOUTUBE_API_KEY,
        "safeSearch": "strict"
    }

    logger.info(f"🔍 Searching YouTube for: '{query}'")
    logger.debug(f"📦 Request params: {params}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(YOUTUBE_SEARCH_URL, params=params) as resp:
                logger.info(f"📡 YouTube API response status: {resp.status}")
                if resp.status != 200:
                    error_text = await resp.text()
                    logger.error(f"❌ YouTube API error: {error_text}")
                    return []

                data = await resp.json()
                logger.debug(f"📊 YouTube API raw response: {data}")

                results = []
                for item in data.get("items", []):
                    video_id = item["id"]["videoId"]
                    snippet = item["snippet"]
                    results.append({
                        "source": "YouTube",
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "url": f"https://www.youtube.com/watch?v={video_id}"
                    })

                logger.info(f"🎥 YouTube returned {len(results)} videos")
                return results

    except Exception as e:
        logger.exception(f"❌ Exception during YouTube search: {e}")
        return []

