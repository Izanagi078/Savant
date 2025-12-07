from typing import Dict, Optional
from src.utils.chunksUtils import simple_token_chunk

def build_video_meta(title: str, platform: str, video_id: str, url: Optional[str] = None) -> Dict:
    if platform.lower() == "youtube":
        url = url or f"https://www.youtube.com/watch?v={video_id}"
    return {"type": "video", "title": title, "platform": platform, "video_id": video_id, "url": url}

def chunk_video_transcript(transcript_text: str, max_chars: int = 1200, overlap: int = 150):
    return simple_token_chunk(transcript_text or "", max_chars=max_chars, overlap=overlap)
