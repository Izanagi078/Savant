import os
import json
import logging
import aiohttp
from sqlalchemy.orm import Session
from src.services.groqService import query_groq, GROQ_API_KEY
from src.services.llmService import GEMINI_API_KEY
from src.models.course import Course
from src.config.mongoConfig import get_mongo_db

logger = logging.getLogger(__name__)

async def chat_tutor(query: str, request_id: str, user_id: int, db: Session) -> dict:
    # 1. Retrieve the course syllabus from PostgreSQL
    course = db.query(Course).filter(Course.id == request_id, Course.user_id == user_id).first()
    context = ""
    
    if course:
        syllabus = course.syllabus
        # We also need to extract flat references for verification
        content_list = []
        for mod in syllabus.get("modules", []):
            for res in mod.get("resources", []):
                content_list.append(res)
                
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

    # 2. Retrieve existing chat history from MongoDB
    try:
        mongo_db = get_mongo_db()
        chat_collection = mongo_db["tutor_chat_sessions"]
        chat_doc = await chat_collection.find_one({"request_id": request_id, "user_id": user_id})
        history = chat_doc.get("history", []) if chat_doc else []
    except Exception as me:
        logger.error(f"Error fetching chat history from MongoDB: {me}")
        history = []

    response_text = ""

    # 3. Call LLM
    if GROQ_API_KEY:
        logger.info(f"⚡ Tutoring chat using Groq API...")
        # Map past history into messages array
        messages = []
        for turn in history[-10:]:
            messages.append({
                "role": "user" if turn["role"] == "user" else "assistant", 
                "content": turn["text"]
            })
        messages.append({"role": "user", "content": query})
        
        response = await query_groq(messages, system_prompt=system_prompt, json_mode=False)
        if "text" in response:
            response_text = response["text"]
        elif "error" in response:
            logger.error(f"Groq chat tutor error: {response['error']}")

    if not response_text and GEMINI_API_KEY:
        logger.info(f"🧠 Tutoring chat using Gemini API fallback...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        # Build prompt string with chat history
        prompt_with_context = f"{system_prompt}\n\n"
        for turn in history[-10:]:
            role_label = "Student" if turn["role"] == "user" else "SmartTutor"
            prompt_with_context += f"{role_label}: {turn['text']}\n"
        prompt_with_context += f"Student: {query}\nSmartTutor:"
        
        payload = {
            "contents": [{"parts": [{"text": prompt_with_context}]}]
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        response_text = res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.error(f"Gemini fallback tutor chat failed: {e}")

    if not response_text:
        response_text = "I am in offline mode due to an API timeout. Please verify your connection keys."

    # 4. Save the new conversation turns to MongoDB
    try:
        new_turns = [
            {"role": "user", "text": query},
            {"role": "tutor", "text": response_text}
        ]
        await chat_collection.update_one(
            {"request_id": request_id, "user_id": user_id},
            {"$push": {"history": {"$each": new_turns}}},
            upsert=True
        )
    except Exception as me:
        logger.error(f"Error persisting new chat turns to MongoDB: {me}")

    return {"response": response_text}
