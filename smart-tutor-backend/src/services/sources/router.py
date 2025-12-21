def route_sources(topic: str) -> list:
    topic = topic.lower()
    if any(word in topic for word in ["ai", "machine learning", "transformer", "recommendation", "llm"]):
        return ["arxiv", "semantic_scholar", "mdpi"]
    if any(word in topic for word in ["gene", "biology", "genetics", "protein", "fox gene"]):
        return ["semantic_scholar", "mdpi", "springer"]
    if any(word in topic for word in ["fox", "animal", "zoology", "ecology"]):
        return ["semantic_scholar", "springer", "jstor"]
    if any(word in topic for word in ["literature", "symbolism", "volpone", "myth"]):
        return ["jstor"]
    if any(word in topic for word in ["charles james fox", "history", "politician"]):
        return ["jstor", "springer"]
    return ["semantic_scholar", "arxiv"]
