from src.models.content import ContentIngestRequest
from src.services.contentAggregator import run_content_aggregator_direct

async def queue_content_request(payload: ContentIngestRequest, request_id: str):
    await run_content_aggregator_direct({
        "request_id": request_id,
        "user_id": payload.user_id,
        "topic": payload.topic,
        "level": payload.level or "beginner",
        "context": payload.context or ""
    })
