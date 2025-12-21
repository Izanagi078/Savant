from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.embeddingsUtils import embed_texts
from src.utils.logger import logger
import numpy as np

def filter_articles(topic: str, context: str, raw_articles: List[Dict], top_k: int = 5) -> List[Dict]:
    if not raw_articles:
        logger.warning("No raw articles to filter.")
        return []

    logger.info(f"Filtering {len(raw_articles)} articles for topic relevance...")

    # Combine topic and context for better disambiguation
    query_text = f"{topic} {context}".strip()
    topic_embedding = embed_texts([query_text])  # shape: (1, dim)

    # Prepare article texts (title + snippet)
    article_texts = [
        f"{article['title']} {article.get('snippet', '')}" for article in raw_articles
    ]

    # Embed all articles
    article_embeddings = embed_texts(article_texts)  # shape: (N, dim)

    # Compute cosine similarity
    similarities = cosine_similarity(topic_embedding, article_embeddings)[0]  # shape: (N,)

    # Attach scores to articles
    for i, article in enumerate(raw_articles):
        article["score"] = float(similarities[i])

    # Sort by score descending
    sorted_articles = sorted(raw_articles, key=lambda x: x["score"], reverse=True)

    logger.info(f"Top article score: {sorted_articles[0]['score']:.4f}")
    return sorted_articles[:top_k]
