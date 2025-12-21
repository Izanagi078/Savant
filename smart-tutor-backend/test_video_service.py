import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Optional: confirm the key is loaded
# print("🔑 YOUTUBE_API_KEY:", os.getenv("YOUTUBE_API_KEY"))

from src.services.videoService import search_youtube

async def test():
    topic = "Frog"
    level = "beginner"
    results = await search_youtube(topic, level)
    print(f"\n🔍 Query: {level} {topic} tutorial")
    print(f"🎥 Videos returned: {len(results)}\n")
    for i, video in enumerate(results, 1):
        print(f"{i}. {video['title']}")
        print(f"   {video['url']}\n")

if __name__ == "__main__":
    asyncio.run(test())
