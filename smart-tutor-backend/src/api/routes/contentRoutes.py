# src/api/routes/contentRoutes.py
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from src.api.controllers import contentController

# Router object
router = APIRouter(prefix="/content", tags=["content"])

@router.post("/ingest/pdf")
async def ingest_pdf(
    title: str = Form(...),
    file: UploadFile = File(...),
    source_url: Optional[str] = Form(None)
):
    file_bytes = await file.read()
    ids = contentController.ingest_pdf(title, file_bytes, source_url)
    return {"status": "ok", "ingested_ids": ids}

@router.post("/ingest/web")
async def ingest_web(title: str = Form(...), url: str = Form(...)):
    ids = contentController.ingest_web(title, url)
    return {"status": "ok", "ingested_ids": ids}

@router.post("/ingest/video")
async def ingest_video(
    title: str = Form(...),
    platform: str = Form(...),
    video_id: str = Form(...),
    transcript_text: Optional[str] = Form(None)
):
    ids = contentController.ingest_video(title, platform, video_id, transcript_text)
    return {"status": "ok", "ingested_ids": ids}

@router.post("/ingest/paper")
async def ingest_paper(title: str = Form(...), url: str = Form(...), source: str = Form("arxiv")):
    ids = contentController.ingest_paper(title, url, source)
    return {"status": "ok", "ingested_ids": ids}

@router.post("/search")
async def search(query: str = Form(...), top_k: int = Form(5)):
    results = contentController.search_content(query, top_k)
    formatted = [
        {
            "id": r["id"],
            "title": r.get("title", ""),
            "type": r.get("type", ""),
            "url": r.get("url"),
            "score": r.get("score"),
            "snippet": (r.get("text") or "")[:500]
        }
        for r in results
    ]
    return {"status": "ok", "results": formatted}
