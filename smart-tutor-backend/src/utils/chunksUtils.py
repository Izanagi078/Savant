from typing import List

def simple_token_chunk(text: str, max_chars: int = 1200, overlap: int = 150) -> List[str]:
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks
