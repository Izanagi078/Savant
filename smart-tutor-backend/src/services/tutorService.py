import os
import json
import logging
import aiohttp
from src.services.groqService import query_groq, GROQ_API_KEY
from src.services.llmService import GEMINI_API_KEY
from src.api.controllers.contentController import course_store

logger = logging.getLogger(__name__)

async def chat_tutor(query: str, request_id: str) -> dict:
    course_data = course_store.get(request_id)
    context = ""
    
    if course_data:
        syllabus = course_data.get("syllabus", {})
        content_list = course_data.get("content", [])
        
        context += f"Course Title: {syllabus.get('title', 'Unknown')}\n"
        context += f"Course Description: {syllabus.get('description', '')}\n\n"
        
        context += "Syllabus Modules:\n"
        for idx, mod in enumerate(syllabus.get("modules", [])):
            context += f"- Module {idx+1}: {mod.get('title')}\n  Description: {mod.get('description')}\n  Concepts: {', '.join(mod.get('key_concepts', []))}\n"
        
        context += "\nRelated References:\n"
        for item in content_list:
            context += f"- [{item.get('source')}] {item.get('title')}: {item.get('description')}\n"
    else:
        context = "No specific course context is available for this request."

    system_prompt = (
        "You are SmartTutor, a helpful and intelligent expert teaching assistant. "
        "Your task is to answer the student's question based on the provided Course Context. "
        "Be concise, educational, and reference module concepts or syndicated resources where applicable. "
        f"\n\n--- COURSE CONTEXT ---\n{context}\n----------------------"
    )

    messages = [{"role": "user", "content": query}]

    if GROQ_API_KEY:
        logger.info(f"⚡ Tutoring chat using Groq API...")
        response = await query_groq(messages, system_prompt=system_prompt, json_mode=False)
        if "text" in response:
            return {"response": response["text"]}
        elif "error" in response:
            logger.error(f"Groq chat tutor error: {response['error']}")

    if GEMINI_API_KEY:
        logger.info(f"🧠 Tutoring chat using Gemini API fallback...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        prompt_with_context = f"{system_prompt}\n\nStudent Query: {query}"
        payload = {
            "contents": [{"parts": [{"text": prompt_with_context}]}]
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        text = res["candidates"][0]["content"]["parts"][0]["text"]
                        return {"response": text}
        except Exception as e:
            logger.error(f"Gemini fallback tutor chat failed: {e}")

    logger.warning("⚠️ No LLM API key configured for tutoring. Serving local mock response.")
    return {"response": f"I am in offline mode. Regarding your question: '{query}'. Please configure a valid API key (Gemini/Groq) to enable live interactive chat tutoring."}
