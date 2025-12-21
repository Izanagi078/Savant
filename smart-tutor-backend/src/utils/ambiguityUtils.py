import aiohttp
from sentence_transformers import SentenceTransformer, util
from src.services.sources.semantic_scholar import search as scholar_search

model = SentenceTransformer("all-MiniLM-L6-v2")

async def has_wikipedia_disambiguation(topic: str) -> bool:
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={topic}&prop=pageprops&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return False
            data = await resp.json()
            pages = data.get("query", {}).get("pages", {})
            return any("disambiguation" in p.get("pageprops", {}) for p in pages.values())

async def is_semantically_ambiguous(topic: str) -> bool:
    papers = await scholar_search(topic, "intermediate")
    if len(papers) < 3:
        return False
    texts = [f"{p['title']} {p['description']}" for p in papers]
    embeddings = model.encode(texts, convert_to_tensor=True)
    sim_matrix = util.pytorch_cos_sim(embeddings, embeddings)
    return sim_matrix.mean().item() < 0.4

async def is_ambiguous_topic(topic: str) -> bool:
    wiki = await has_wikipedia_disambiguation(topic)
    semantic = await is_semantically_ambiguous(topic)
    return wiki or semantic
