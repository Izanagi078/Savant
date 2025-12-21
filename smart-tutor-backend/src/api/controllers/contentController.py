from uuid import uuid4
from fastapi import APIRouter, HTTPException
from src.models.content import ContentIngestRequest, ContentIngestResponse
from src.services.contentService import queue_content_request
from src.services.redisService import get_content

router = APIRouter()

@router.post("/ingest", response_model=ContentIngestResponse)
async def ingest_content(payload: ContentIngestRequest):
    request_id = str(uuid4())
    await queue_content_request(payload, request_id)
    return ContentIngestResponse(
        status="queued",
        topic=payload.topic,
        request_id=request_id,
        videos=[],
        papers=[],
        resources=[]
    )

@router.get("/status/{request_id}", response_model=ContentIngestResponse)
async def get_content_status(request_id: str):
    data = await get_content(request_id)
    if not data or "results" not in data:
        raise HTTPException(status_code=404, detail="No content found")

    topic = data.get("topic", "unknown")
    results = data["results"]

    return ContentIngestResponse(
        status="completed",
        topic=topic,
        request_id=request_id,
        videos=[r for r in results if r.get("source") == "YouTube"],
        papers=[r for r in results if r.get("source") == "PDF"], 
        resources=[r for r in results if r.get("source") == "Web"]
    )

