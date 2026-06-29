import os
import json
import logging
import aiohttp
from src.services.groqService import query_groq, GROQ_API_KEY
from src.services.llmService import GEMINI_API_KEY

logger = logging.getLogger(__name__)

async def generate_quiz(topic: str, count: int = 4) -> dict:
    prompt = (
        f"Design a multiple-choice quiz about '{topic}' containing exactly {count} questions. "
        "Each question must test conceptual understanding and list 3 to 4 plausible options. "
        "Enforce JSON format containing a list of 'questions', where each question has fields: "
        "'id' (integer), 'text' (string), 'options' (array of strings), and 'answer' (integer index of the correct option, 0-indexed)."
    )

    if GROQ_API_KEY:
        logger.info(f"⚡ Generating quiz for '{topic}' using Groq API...")
        system_prompt = "You are a professional educational assessor. You output raw, valid JSON."
        messages = [{"role": "user", "content": prompt}]
        response = await query_groq(messages, system_prompt=system_prompt, json_mode=True)
        if "questions" in response:
            return response
        else:
            logger.warning(f"Groq quiz response didn't contain 'questions' list: {response}")

    if GEMINI_API_KEY:
        logger.info(f"🧠 Generating quiz for '{topic}' using Gemini API fallback...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "questions": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "id": {"type": "INTEGER"},
                                    "text": {"type": "STRING"},
                                    "options": {
                                        "type": "ARRAY",
                                        "items": {"type": "STRING"}
                                    },
                                    "answer": {"type": "INTEGER"}
                                },
                                "required": ["id", "text", "options", "answer"]
                            }
                        }
                    },
                    "required": ["questions"]
                }
            }
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        text = res["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(text)
        except Exception as e:
            logger.error(f"Failed to generate quiz using Gemini fallback: {e}")

    logger.warning("⚠️ No LLM API key configured for quiz generation. Serving local mock quiz.")
    return get_mock_quiz(topic)

def get_mock_quiz(topic: str) -> dict:
    return {
        "questions": [
            {
                "id": 1,
                "text": f"Which of the following best describes the core concept of {topic}?",
                "options": [
                    "A tool primarily used for manual filesystem operations",
                    "A set of design principles for optimizing cloud database scaling",
                    "A domain-specific mechanism matching user-defined educational parameters",
                    "None of the above"
                ],
                "answer": 2
            },
            {
                "id": 2,
                "text": f"Why is performance optimization critical when structuring learning pathways in {topic}?",
                "options": [
                    "To prevent visual assets from loading slowly",
                    "To decrease latency and ensure high student engagement rates",
                    "To minimize CPU utilization during offline evaluations",
                    "To satisfy standard linter criteria"
                ],
                "answer": 1
            }
        ]
    }
