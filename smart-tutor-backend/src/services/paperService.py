from typing import Dict

def build_paper_meta(title: str, url: str, source: str = "arxiv") -> Dict:
    return {"type": "paper", "title": title, "url": url, "source": source}
