from src.models.content import ContentIngestRequest
from src.services.kafkaService import emit_event

async def queue_content_request(payload: ContentIngestRequest, request_id: str):
    await emit_event("user_prompt", {
        "request_id": request_id,
        "user_id": payload.user_id,
        "topic": payload.topic,
        "level": payload.level or "beginner"
    })
