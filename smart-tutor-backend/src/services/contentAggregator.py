import logging
from src.services.videoService import search_youtube
from src.services.articlePipeline import run_article_pipeline
from src.services.redisService import save_content
from src.services.paperPipeline.run_paper_pipeline import run_paper_pipeline  # ✅ Updated import

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_content_aggregator_direct(data: dict):
    topic = data.get("topic")
    level = data.get("level")
    context = data.get("context", "")
    request_id = data.get("request_id")

    if not request_id:
        logger.warning(f"⚠️ Missing request_id in message: {data}")
        return

    if not level:
        logger.info(f"ℹ️ No level provided — defaulting to 'beginner'")
        level = "beginner"

    logger.info(f"📥 Processing content aggregation for: {topic} | Level: {level} | Request ID: {request_id}")

    try:
        # Fetch YouTube videos
        videos = await search_youtube(topic, level, context)

        # Fetch and filter articles using ML pipeline
        articles = run_article_pipeline(topic, level, context)
        for article in articles:
            article["source"] = "Web"

        # Fetch academic papers (only for advanced level)
        papers = []
        if level.lower() == "advanced":
            logger.info(f"📚 Fetching academic papers for: {topic}")
            paper_links = run_paper_pipeline(topic, context)  # ✅ Now sync
            logger.info(f"📄 Found {len(paper_links)} PDF links")
            papers = [{"title": link.split('/')[-1], "url": link, "source": "PDF"} for link in paper_links]

        # Combine all content
        all_content = videos + articles + papers

        # Save to Redis
        await save_content(request_id, {
            "topic": topic,
            "context": context,
            "videos": videos,
            "resources": articles + papers,
            "results": all_content
        })

        logger.info(f"✅ Successfully saved content for request_id: {request_id}")

    except Exception as e:
        logger.error(f"❌ Error processing topic '{topic}' (request_id: {request_id}): {e}")
