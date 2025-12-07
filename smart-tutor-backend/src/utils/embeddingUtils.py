from langchain_community.embeddings import HuggingFaceEmbeddings

_embeddings = None

def get_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return _embeddings

def embed_texts(texts: list[str]) -> list[list[float]]:
    return get_embeddings().embed_documents(texts)

def embed_query(text: str) -> list[float]:
    return get_embeddings().embed_query(text)
