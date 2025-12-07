from typing import List, Dict, Any
from src.services.vectorDBService import store

def aggregate_search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    return store.search(query, top_k=top_k)
