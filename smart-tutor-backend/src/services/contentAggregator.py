import json
import asyncio
from uuid import uuid4
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from datetime import datetime
import logging

from src.services.videoService import search_youtube
from src.services.paperService import search_arxiv
from src.services.resourceService import search_articles
from src.services.redisService import save_content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
INPUT_TOPIC = "user_prompt"
OUTPUT_TOPIC = "raw_content_fetched"

async def run_content_aggregator():
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="content-aggregator-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda m: json.dumps(m).encode("utf-8")
    )

    await consumer.start()
    await producer.start()
    logger.info(f"🟢 Content Aggregator is running and listening on '{INPUT_TOPIC}'...")

    try:
        async for msg in consumer:
            data = msg.value
            topic = data.get("topic")
            level = data.get("level", "beginner")
            request_id = data.get("request_id")

            if not request_id:
                logger.warning(f"⚠️ Missing request_id in message: {data}")
                continue

            logger.info(f"📥 Received: {data}")

            try:
                videos = await search_youtube(topic, level)
                papers = await search_arxiv(topic, level)
                articles = await search_articles(topic, level)

                logger.info(f"🎥 Found {len(videos)} videos")
                logger.info(f"📄 Found {len(papers)} papers")
                logger.info(f"📚 Found {len(articles)} articles")

                all_content = videos + papers + articles

                await save_content(request_id, all_content)
                logger.info(f"💾 Saved content to Redis for request_id: {request_id}")

                for item in all_content:
                    payload = {
                        "request_id": request_id,
                        "source": item["source"],
                        "title": item["title"],
                        "description": item["description"],
                        "url": item["url"],
                        "timestamp": datetime.utcnow().isoformat()
                    }

                    await producer.send_and_wait(
                        topic=OUTPUT_TOPIC,
                        key=str(uuid4()).encode("utf-8"),
                        value=payload
                    )

                logger.info(f"✅ Published {len(all_content)} items for topic: {topic}")

            except Exception as e:
                logger.error(f"❌ Error processing topic '{topic}': {e}")

    finally:
        await consumer.stop()
        await producer.stop()
        logger.info("🛑 Content Aggregator stopped.")
if __name__ == "__main__":
    asyncio.run(run_content_aggregator())

