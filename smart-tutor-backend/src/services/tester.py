import asyncio
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the project root, two levels up from this file
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

# Optional: confirm the key is loaded
# print("🔑 YOUTUBE_API_KEY:", os.getenv("YOUTUBE_API_KEY"))

from videoService import search_youtube

async def test():
    topic = "the"
    level = "beginner"
    results = await search_youtube(topic, level)
    print(f"\n🔍 Query: {level} {topic} tutorial")
    print(f"🎥 Videos returned: {len(results)}\n")
    for i, video in enumerate(results, 1):
        print(f"{i}. {video['title']}")
        print(f"   {video['url']}\n")

if __name__ == "__main__":
    asyncio.run(test())
