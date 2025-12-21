from src.services.paperPipeline.fetchDuckDuckGo import fetch_pdf_links
from src.services.paperPipeline.scorePDFs import score_pdfs
from src.utils.logger import logger

def run_paper_pipeline(topic: str, context: str, top_k: int = 5) -> list:
    logger.info(f"📚 Running paper pipeline for: {topic}")
    pdf_links = fetch_pdf_links(topic, context, min_links=10)
    if not pdf_links:
        logger.warning("⚠️ No PDF links found")
        return []
    return score_pdfs(pdf_links, f"{topic} {context}", top_k)
