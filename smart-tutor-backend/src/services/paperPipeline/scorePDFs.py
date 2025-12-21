from src.utils.parserUtils import extract_text_from_pdf
from src.utils.embeddingUtils import get_embedding, cosine_similarity
from src.services.paperPipeline.validatePDF import is_valid_pdf_url
from src.utils.logger import logger

def score_pdfs(pdf_links: list, query: str, top_k: int = 5) -> list:
    query_embedding = get_embedding(query)
    scored_links = []

    for url in pdf_links:
        if not is_valid_pdf_url(url):
            logger.debug(f"[PDF] Skipping non-PDF or inaccessible URL: {url}")
            continue
        try:
            logger.debug(f"[PDF] Scoring: {url}")
            text = extract_text_from_pdf(url)
            if not text:
                logger.debug(f"[PDF] No text extracted from {url}")
                continue
            score = cosine_similarity(query_embedding, get_embedding(text[:1000]))
            logger.debug(f"[PDF] Relevance score: {score:.4f}")
            scored_links.append((url, score))
        except Exception as e:
            logger.error(f"[PDF] Failed to process {url}: {e}")
            continue

    scored_links.sort(key=lambda x: x[1], reverse=True)
    return [url for url, _ in scored_links[:top_k]]
