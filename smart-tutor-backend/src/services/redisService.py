import redis.asyncio as redis
import json
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ✅ Use localhost since Redis is running in Docker and exposed to host
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

async def save_content(request_id: str, content: dict, ttl: int = 3600):
    try:
        await r.set(request_id, json.dumps(content), ex=ttl)
        logger.info(f"[REDIS] Saved content for request_id: {request_id}")
    except Exception as e:
        logger.error(f"[REDIS] Failed to save content for {request_id}: {e}")

async def get_content(request_id: str) -> Optional[dict]:
    try:
        data = await r.get(request_id)
        if data is None:
            logger.warning(f"[REDIS] No data found for request_id: {request_id}")
            return None
        return json.loads(data)
    except Exception as e:
        logger.error(f"[REDIS] Failed to retrieve or parse content for {request_id}: {e}")
        return None
