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
    results = await get_content(request_id)
    if not results:
        raise HTTPException(status_code=404, detail="No content found")

    topic = "unknown"
    for item in results:
        if "title" in item and item["title"]:
            topic = item["title"].split()[0]
            break

    return ContentIngestResponse(
        status="completed",
        topic=topic,
        request_id=request_id,
        videos=[r for r in results if r.get("source") == "YouTube"],
        papers=[r for r in results if r.get("source") == "arXiv"],
        resources=[r for r in results if r.get("source") == "Web"]
    )
