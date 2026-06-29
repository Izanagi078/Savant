import os
import json
import logging
from src.services.groqService import query_groq, GROQ_API_KEY
from src.services.llmService import GEMINI_API_KEY
import aiohttp

logger = logging.getLogger(__name__)

async def verify_and_map_resources(syllabus_with_raw_resources: dict, level: str) -> dict:
    """
    Evaluates raw resources (YouTube, arXiv, Wikipedia/Web) for each module in the syllabus
    against the target difficulty level and module concepts. Filters out resources that
    are too complex or irrelevant, and maps the best/verified resources directly to the module.
    """
    system_prompt = (
        "You are an expert educational auditor and verifier. "
        f"Your task is to review a course syllabus designed for a '{level}' level student. "
        "Each module contains a list of candidate resources fetched from YouTube, arXiv, and Wikipedia/Web. "
        "For each resource, evaluate its relevance to the module concepts and its suitability for the student's difficulty level.\n\n"
        "Guidelines for verification:\n"
        f"- Target Level is '{level}'.\n"
        "- If a resource (especially from arXiv) contains highly advanced formulas, deep technical jargon, or complex papers inappropriate for the level, FILTER IT OUT.\n"
        "- If a video or page is irrelevant to the module's key concepts, FILTER IT OUT.\n"
        "- Only retain high-quality resources that directly aid in learning the module's core concepts at the specified level.\n"
        "- Do not make up resources or URLs. Only choose from the provided candidates.\n"
        "- Return the updated course structure in JSON format matching the schema below."
    )

    prompt = (
        f"Review the following course structure and candidate resources. Return a JSON object containing the course title, "
        "description, and the list of modules. Each module must contain its title, description, key_concepts, and a list of "
        "verified 'resources' (under a 'resources' key), with all unqualified or too difficult resources filtered out.\n\n"
        "Input Data:\n"
        f"{json.dumps(syllabus_with_raw_resources, indent=2)}\n\n"
        "Return the output in this JSON format:\n"
        "{\n"
        '  "title": "Course Title",\n'
        '  "description": "Course Description",\n'
        '  "modules": [\n'
        "    {\n"
        '      "title": "Module Title",\n'
        '      "description": "Module Description",\n'
        '      "key_concepts": ["concept1", "concept2"],\n'
        '      "resources": [\n'
        "        {\n"
        '          "source": "YouTube" | "arXiv" | "Wikipedia",\n'
        '          "title": "Resource Title",\n'
        '          "description": "Brief verified description or justification why this is helpful",\n'
        '          "url": "Resource URL"\n'
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    # Attempt to query Groq first
    if GROQ_API_KEY:
        try:
            logger.info("Querying Groq Llama 3.1 for resource verification...")
            response = await query_groq(
                messages=[{"role": "user", "content": prompt}],
                system_prompt=system_prompt,
                json_mode=True,
                model="llama-3.1-8b-instant"
            )
            if "error" not in response:
                return response
            logger.warning(f"Groq verification failed or returned error: {response.get('error')}. Falling back to Gemini.")
        except Exception as e:
            logger.error(f"Error querying Groq in verifierAgent: {e}. Falling back to Gemini.")

    # Fallback to Gemini
    if GEMINI_API_KEY:
        try:
            logger.info("Querying Gemini 1.5 Flash for resource verification (fallback)...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": f"{system_prompt}\n\nInput Data and Task:\n{prompt}"}
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
                                        "resources": {
                                            "type": "ARRAY",
                                            "items": {
                                                "type": "OBJECT",
                                                "properties": {
                                                    "source": {"type": "STRING"},
                                                    "title": {"type": "STRING"},
                                                    "description": {"type": "STRING"},
                                                    "url": {"type": "STRING"}
                                                },
                                                "required": ["source", "title", "description", "url"]
                                            }
                                        }
                                    },
                                    "required": ["title", "description", "key_concepts", "resources"]
                                }
                            }
                        },
                        "required": ["title", "description", "modules"]
                    }
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(text_content)
                    else:
                        error_text = await resp.text()
                        logger.error(f"Gemini API returned error {resp.status}: {error_text}")
        except Exception as e:
            logger.error(f"Error querying Gemini for verification: {e}")

    # Final mock/unverified fallback mapping if both APIs are unavailable or fail
    logger.warning("All LLM APIs failed for verification. Returning raw/unverified fallback mapping.")
    return get_unverified_fallback_mapping(syllabus_with_raw_resources, level)

def get_unverified_fallback_mapping(syllabus_with_raw_resources: dict, level: str) -> dict:
    modules = []
    for mod in syllabus_with_raw_resources.get("modules", []):
        verified_resources = []
        raw_res = mod.get("raw_resources", {})
        
        # Simple heuristic: arXiv papers might be filtered out if level is beginner
        for source, items in raw_res.items():
            for item in items:
                # Basic heuristic filtering: if beginner, drop arxiv paper containing words like "Theoretical", "Quantum", "Proof"
                if level.lower() == "beginner" and source == "arxiv":
                    title_lower = item.get("title", "").lower()
                    desc_lower = item.get("description", "").lower()
                    if any(w in title_lower or w in desc_lower for w in ["quantum", "theoretical", "proof", "complexity", "mathematical"]):
                        continue # filter out complex papers
                verified_resources.append({
                    "source": "YouTube" if source == "youtube" else ("arXiv" if source == "arxiv" else "Wikipedia"),
                    "title": item.get("title", "Resource"),
                    "description": item.get("description", ""),
                    "url": item.get("url", "")
                })
        
        modules.append({
            "title": mod.get("title", "Module"),
            "description": mod.get("description", ""),
            "key_concepts": mod.get("key_concepts", []),
            "resources": verified_resources
        })

    return {
        "title": syllabus_with_raw_resources.get("title", "Course"),
        "description": syllabus_with_raw_resources.get("description", ""),
        "modules": modules
    }
