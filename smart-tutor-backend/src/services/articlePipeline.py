from typing import List, Dict
from src.services.articleFetcher import fetch_articles
from src.services.articleFilter import filter_articles
from src.utils.summarizerUtils import summarize_articles
from src.utils.logger import logger

def run_article_pipeline(topic: str, level: str, context: str = "", top_k: int = 5) -> List[Dict]:
    logger.info(f"Running article pipeline for topic: {topic}, level: {level}, context: {context}")

    # Step 1: Scrape raw articles
    raw_articles = fetch_articles(topic, level, context)
    if not raw_articles:
        logger.warning("No articles fetched.")
        return []

    # Step 2: Filter using semantic similarity with context
    filtered_articles = filter_articles(topic, context, raw_articles, top_k=top_k)

    # Step 3: Summarize top articles
    summarized_articles = summarize_articles(filtered_articles)

    return summarized_articles
