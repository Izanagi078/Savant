from transformers import pipeline
from typing import List, Dict
from src.utils.logger import logger

# Load once at module level
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_articles(articles: List[Dict], max_tokens: int = 512) -> List[Dict]:
    logger.info(f"Summarizing {len(articles)} articles...")

    for article in articles:
        text = article.get("snippet", "")
        if not text or len(text.split()) < 30:
            article["summary"] = text  # Skip short snippets
            continue

        try:
            summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
            article["summary"] = summary
        except Exception as e:
            logger.warning(f"Summarization failed for article: {article['title']} — {e}")
            article["summary"] = text  # Fallback to original snippet

    return articles
