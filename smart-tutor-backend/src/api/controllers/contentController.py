# src/controllers/contentController.py
from typing import List
from src.services.vectorDBService import store
from src.services.videoService import build_video_meta, chunk_video_transcript
from src.services.paperService import build_paper_meta
from src.services.kafkaService import emit_event
from src.utils.parserUtils import parse_pdf, parse_web
from src.utils.chunksUtils import simple_token_chunk

def ingest_pdf(title: str, file_bytes: bytes, source_url: str | None = None) -> List[str]:
    raw_text = parse_pdf(file_bytes)
    chunks = simple_token_chunk(raw_text)
    ids = store.add(chunks, {"type": "pdf", "title": title, "url": source_url})
    emit_event("content_ingestion", {"type": "pdf", "title": title, "url": source_url, "count": len(ids)})
    return ids

def ingest_web(title: str, url: str) -> List[str]:
    raw_text = parse_web(url)
    chunks = simple_token_chunk(raw_text)
    ids = store.add(chunks, {"type": "web", "title": title, "url": url})
    emit_event("content_ingestion", {"type": "web", "title": title, "url": url, "count": len(ids)})
    return ids

def ingest_video(title: str, platform: str, video_id: str, transcript_text: str | None = None) -> List[str]:
    meta = build_video_meta(title, platform, video_id)
    chunks = chunk_video_transcript(transcript_text) if transcript_text else []
    ids = store.add(chunks, meta) if chunks else []
    emit_event("content_ingestion", {**meta, "count": len(ids)})
    return ids

def ingest_paper(title: str, url: str, source: str = "arxiv") -> List[str]:
    meta = build_paper_meta(title, url, source)
    ids = store.add([f"{title} - {url}"], meta)
    emit_event("content_ingestion", {**meta, "count": len(ids)})
    return ids

def search_content(query: str, top_k: int = 5):
    emit_event("content_query", {"type": "query", "query": query, "top_k": top_k})
    return store.search(query, top_k=top_k)
