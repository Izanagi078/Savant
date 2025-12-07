# src/services/vectorDBService.py
import faiss
import numpy as np
import uuid
import os
import json
from typing import List, Dict, Any
from src.utils.embeddingUtils import embed_texts, embed_query

INDEX_PATH = "data/faiss.index"
META_PATH = "data/meta.jsonl"
DIM = 384  # Embedding dimension

class VectorDBService:
    def __init__(self):
        self.index = None
        self.metadata: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            if os.path.exists(META_PATH):
                with open(META_PATH, "r", encoding="utf-8") as f:
                    self.metadata = [json.loads(line) for line in f]
        else:
            self.index = faiss.IndexFlatIP(DIM)

    def _persist(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "w", encoding="utf-8") as f:
            for m in self.metadata:
                f.write(json.dumps(m) + "\n")

    def add(self, chunks: List[str], base_meta: Dict[str, Any]) -> List[str]:
        vectors = np.array(embed_texts(chunks)).astype("float32")
        faiss.normalize_L2(vectors)
        ids = [str(uuid.uuid4()) for _ in chunks]
        self.index.add(vectors)
        for i, chunk in enumerate(chunks):
            meta = {"id": ids[i], "text": chunk, **base_meta}
            self.metadata.append(meta)
        self._persist()
        return ids

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q = np.array(embed_query(query)).astype("float32").reshape(1, -1)
        faiss.normalize_L2(q)
        D, I = self.index.search(q, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1: continue
            m = self.metadata[idx]
            results.append({"score": float(score), **m})
        return results

store = VectorDBService()
