import os
import aiohttp
import json
import logging

logger = logging.getLogger(__name__)

def load_env():
    for env_path in [".env", "../.env", "smart-tutor-backend/.env"]:
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip()
            break

load_env()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def generate_syllabus(topic: str, level: str = "beginner") -> dict:
    if not GEMINI_API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY is not set. Using local mock generator fallback.")
        return get_mock_syllabus(topic, level)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = (
        f"You are an expert tutor. Design a comprehensive course syllabus about '{topic}' for a '{level}' level student. "
        "Break the course down into a structured path of 3 to 4 learning modules. "
        "Provide clear, educational titles, descriptions, and a list of key concepts for each module. "
        f"Additionally, output three highly targeted, simple search queries for each module to retrieve supplementary materials suitable for a '{level}' level student: "
        "one query specifically for YouTube video guides, one for arXiv research papers/abstracts, and one for Wikipedia pages.\n\n"
        "Crucial Search Query Guidelines:\n"
        "- Do NOT include noise words like 'youtube', 'arxiv', 'wikipedia', 'video', 'paper', 'article', 'tutorial', 'beginner', 'intermediate', 'advanced' in the search queries.\n"
        "- Keep the queries focused on the core concept name. For example, if the module is about 'Introduction to Derivatives', the search queries should simply be:\n"
        "  * youtube: 'derivatives introduction'\n"
        "  * arxiv: 'calculus derivatives'\n"
        "  * wikipedia: 'derivative'\n\n"
        "Example of structured response format:\n"
        "{\n"
        '  "title": "Introduction to Calculus",\n'
        '  "description": "A beginner course on limits, derivatives, and basic integration.",\n'
        '  "modules": [\n'
        "    {\n"
        '      "title": "Limits and Continuity",\n'
        '      "description": "Understanding the foundational limit concept in calculus.",\n'
        '      "key_concepts": ["Limit Definition", "One-Sided Limits", "Continuity"],\n'
        '      "search_queries": {\n'
        '        "youtube": "calculus limits introduction",\n'
        '        "arxiv": "calculus limits",\n'
        '        "wikipedia": "limit of a function"\n'
        "      }\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "description": {"type": "STRING"},
                    "modules": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "title": {"type": "STRING"},
                                "description": {"type": "STRING"},
                                "key_concepts": {
                                    "type": "ARRAY",
                                    "items": {"type": "STRING"}
                                },
                                "search_queries": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "youtube": {"type": "STRING"},
                                        "arxiv": {"type": "STRING"},
                                        "wikipedia": {"type": "STRING"}
                                    },
                                    "required": ["youtube", "arxiv", "wikipedia"]
                                }
                            },
                            "required": ["title", "description", "key_concepts", "search_queries"]
                        }
                    }
                },
                "required": ["title", "description", "modules"]
            }
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(text_content)
                else:
                    error_text = await resp.text()
                    logger.error(f"Gemini API returned error {resp.status}: {error_text}")
                    return get_mock_syllabus(topic, level)
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return get_mock_syllabus(topic, level)

def get_mock_syllabus(topic: str, level: str) -> dict:
    return {
        "title": f"Mastering {topic.title()}",
        "description": f"A comprehensive {level}-level guide designed to take you from core concepts to advanced paradigms in {topic}.",
        "modules": [
            {
                "title": f"Module 1: Foundations of {topic.title()}",
                "description": f"An introductory look into the basic mechanics, history, and core terminology of {topic}.",
                "key_concepts": ["Core Definitions", "Historical Context", "Fundamental Axioms"],
                "search_queries": {
                    "youtube": f"beginner {topic} foundations tutorial",
                    "arxiv": f"introduction to {topic} overview paper",
                    "wikipedia": f"{topic} definition basics"
                }
            },
            {
                "title": f"Module 2: Practical Implementations",
                "description": "Hands-on application of concepts, common workflows, and building your first projects.",
                "key_concepts": ["Environment Configuration", "Standard Patterns", "Best Practices"],
                "search_queries": {
                    "youtube": f"{topic} practical setup guide",
                    "arxiv": f"implementing {topic} system architectures",
                    "wikipedia": f"{topic} applications cases"
                }
            }
        ]
    }
