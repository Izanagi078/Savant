import aiohttp

async def search_articles(topic: str, level: str) -> list:
    query = f"{level} {topic}"
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query.replace(' ', '+')}&limit=3&namespace=0&format=json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return get_fallback_articles(topic, level)
                data = await resp.json()
                results = []
                
                if len(data) >= 4:
                    titles = data[1]
                    descriptions = data[2]
                    links = data[3]
                    
                    for i in range(min(len(titles), 3)):
                        title = titles[i]
                        desc = descriptions[i] if descriptions[i] else f"Learn details about {title}."
                        link = links[i]
                        
                        results.append({
                            "source": "Web",
                            "title": title,
                            "description": desc,
                            "url": link
                        })

                if not results:
                    return get_fallback_articles(topic, level)
                return results
        except Exception:
            return get_fallback_articles(topic, level)

def get_fallback_articles(topic: str, level: str) -> list:
    return [
        {
            "source": "Web",
            "title": f"Introduction to {topic.title()}",
            "description": f"A comprehensive introduction and reference manual to understand {topic} core paradigms.",
            "url": f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        },
        {
            "source": "Web",
            "title": f"Best Practices for {topic.title()} Development",
            "description": f"Guidelines and industry standards to streamline your learning curve in {topic}.",
            "url": "https://geeksforgeeks.org"
        }
    ]
