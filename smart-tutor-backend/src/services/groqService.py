import os
import aiohttp
import json
import logging

logger = logging.getLogger(__name__)

def load_env():
    # Attempt to load from parent or local .env file
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

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def query_groq(messages: list, system_prompt: str = None, json_mode: bool = False, model: str = "llama-3.1-8b-instant") -> dict:
    if not GROQ_API_KEY:
        logger.warning("⚠️ GROQ_API_KEY is not set. Cannot hit Groq API.")
        return {"error": "GROQ_API_KEY not configured"}

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    formatted_messages = []
    if system_prompt:
        formatted_messages.append({"role": "system", "content": system_prompt})
    formatted_messages.extend(messages)

    payload = {
        "model": model,
        "messages": formatted_messages,
        "temperature": 0.2
    }

    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"]
                    if json_mode:
                        try:
                            return json.loads(content)
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse JSON response from Groq: {content}")
                            return {"raw_text": content, "error": "JSON parse error"}
                    return {"text": content}
                else:
                    error_text = await resp.text()
                    logger.error(f"Groq API returned error {resp.status}: {error_text}")
                    return {"error": f"Groq API error {resp.status}"}
    except Exception as e:
        logger.error(f"Error querying Groq: {e}")
        return {"error": str(e)}
