import os
import json
import logging
import aiohttp
from src.services.llmService import query_groq, GROQ_API_KEY, GEMINI_API_KEY

logger = logging.getLogger(__name__)

# Strict difficulty criteria to guide both Generator and Verifier Agent
LEVEL_GUIDELINES = {
    "Beginner": "Focus on foundational concepts, basic definitions, and single-step applications of formulas. Avoid multi-step calculations or advanced nuances.",
    "Intermediate": "Focus on standard application of core principles, standard problem-solving, and basic multi-step analysis (2-3 steps). Requires solid understanding but avoids extreme edge cases or highly rigorous derivations.",
    "Advanced": "Focus on university/graduate level complexity. The questions must require rigorous mathematical/scientific derivations, complex multi-step reasoning (4+ steps), or deep conceptual synthesis of multiple advanced principles. Avoid any introductory concepts, simple formula applications, or standard textbook problems. Every question must be genuinely challenging and require high analytical capability."
}

def validate_quiz_data(quiz_data: dict, expected_count: int) -> bool:
    if not isinstance(quiz_data, dict):
        return False
    questions = quiz_data.get("questions")
    if not isinstance(questions, list) or len(questions) != expected_count:
        return False
    for q in questions:
        if not isinstance(q, dict):
            return False
        if not all(k in q for k in ("id", "text", "options", "explanation", "answer")):
            return False
        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            return False
        if not isinstance(q["answer"], int) or not (0 <= q["answer"] <= 3):
            return False
    return True

async def generate_quiz(topic: str, count: int = 10, level: str = "Beginner") -> dict:
    """
    Generates a multiple-choice quiz of exactly `count` questions with 4 options each,
    tailored to `level` difficulty using strict guidelines.
    """
    logger.info(f"Generating initial {count}-question quiz on '{topic}' at '{level}' level...")
    
    initial_quiz = await generate_quiz_batch(topic, count, level)

    if not initial_quiz or not initial_quiz.get("questions"):
        logger.warning("⚠️ All LLM APIs failed. Serving local mock quiz.")
        return get_mock_quiz(topic, count)

    if validate_quiz_data(initial_quiz, count):
        logger.info("✅ Quiz successfully passed local critic validation. Skipping verifier agent call.")
        return initial_quiz

    logger.warning("⚠️ Local validation failed. Invoking Quiz Verifier Agent to audit and check the questions.")
    try:
        verified_quiz = await verify_quiz_questions(initial_quiz, topic, level)
        if validate_quiz_data(verified_quiz, count):
            return verified_quiz
    except Exception as e:
        logger.error(f"Quiz Verifier Agent error: {e}.")
        
    if len(initial_quiz.get("questions", [])) > 0:
        return initial_quiz
    return get_mock_quiz(topic, count)

async def generate_quiz_batch(topic: str, count: int, level: str) -> dict:
    """
    Generates questions using Gemini (preferred due to high token limit) or Groq APIs.
    """
    guideline = LEVEL_GUIDELINES.get(level, LEVEL_GUIDELINES["Beginner"])
    
    prompt = (
        f"Design a multiple-choice quiz about '{topic}' for a '{level}' level student containing exactly {count} questions.\n"
        f"Difficulty constraints for '{level}' level: {guideline}\n\n"
        "Instructions:\n"
        "- Each question must test conceptual understanding at this exact difficulty level.\n"
        "- Provide exactly 4 plausible options for each question.\n"
        "- For each question, perform any required mathematical calculations or reasoning step-by-step and write it down in the 'explanation' field.\n"
        "- Do NOT use LaTeX backslashes or LaTeX formatting. Write all mathematical expressions and symbols in plain text or standard calculator/ASCII notation.\n"
        "- Enforce JSON format containing a list of 'questions', where each question has fields: "
        "'id' (integer), 'text' (string), 'options' (array of strings of exactly 4 choices), 'explanation' (detailed step-by-step calculation or reasoning), and 'answer' (integer index of correct option, 0-indexed)."
    )

    initial_quiz = None

    # Prioritize Gemini 2.5 Flash for high TPM limits
    if GEMINI_API_KEY:
        try:
            logger.info(f"🧠 Generating quiz of {count} questions using Gemini 2.5 Flash...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
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
                                        "explanation": {"type": "STRING"},
                                        "answer": {"type": "INTEGER"}
                                    },
                                    "required": ["id", "text", "options", "explanation", "answer"]
                                }
                            }
                        },
                        "required": ["questions"]
                    }
                }
            }
            timeout = aiohttp.ClientTimeout(total=180)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        text = res["candidates"][0]["content"]["parts"][0]["text"]
                        initial_quiz = json.loads(text)
        except Exception as e:
            logger.error(f"Gemini quiz generation failed: {e}")

    # Fallback to Groq if Gemini fails or is not configured
    if not initial_quiz and GROQ_API_KEY:
        try:
            logger.info(f"⚡ Generating quiz of {count} questions using Groq API fallback...")
            system_prompt = f"You are a professional educational assessor. You output raw, valid JSON. Target level is {level}."
            messages = [{"role": "user", "content": prompt}]
            response = await query_groq(messages, system_prompt=system_prompt, json_mode=True, model="llama-3.3-70b-versatile")
            if "questions" in response:
                initial_quiz = response
        except Exception as e:
            logger.error(f"Groq fallback quiz generation failed: {e}")

    return initial_quiz or {"questions": []}

async def verify_quiz_questions(quiz_data: dict, topic: str, level: str) -> dict:
    """
    Quiz Verifier Agent: audits generated questions against difficulty level, option counts, and answer key accuracy.
    """
    logger.info(f"🤖 Quiz Verifier Agent running level check for '{level}' level...")
    guideline = LEVEL_GUIDELINES.get(level, LEVEL_GUIDELINES["Beginner"])
    
    system_prompt = (
        "You are an expert educational auditor and quiz verifier. "
        f"Your task is to audit multiple-choice questions designed for a '{level}' level student on the topic of '{topic}'.\n\n"
        f"Difficulty constraints for '{level}' level: {guideline}\n\n"
        "Audit guidelines:\n"
        f"- Target Level is '{level}'. You must be extremely strict about this. If a question is too basic, too simple, or does not meet the '{level}' level guidelines, you MUST completely rewrite or replace it with a new, highly compliant question at the correct difficulty level.\n"
        "- Perform rigorous mathematical and factual verification on every question. Read the 'explanation' field, solve the problem step-by-step to verify the calculation, and correct any arithmetic, algebraic, or integration errors in the question text, options, explanation, or correct answer index.\n"
        "- Do NOT use LaTeX backslashes or LaTeX formatting (e.g., do NOT use '\\int', '\\frac', '\\pi', '\\sqrt', or math delimiters like '$'). Write all mathematical expressions, formulas, and symbols in plain text or standard calculator/ASCII notation.\n"
        "- Ensure every single question has EXACTLY 4 options in the options array.\n"
        "- Verify that the 'answer' field holds the correct 0-based index of the right option in the options array.\n"
        "- Do not omit any questions. Output the final audited and corrected quiz in the same JSON structure with 'id', 'text', 'options', 'explanation', and 'answer' fields."
    )

    prompt = (
        f"Please audit the following quiz data. Inspect every question to ensure difficulty level suitability for a '{level}' level student, "
        "verify that the correct answer is indeed correct, and ensure exactly 4 options are present per question.\n\n"
        f"Input Quiz Data:\n{json.dumps(quiz_data, indent=2)}\n\n"
        "Return the audited JSON object matching this schema:\n"
        "{\n"
        '  "questions": [\n'
        "    {\n"
        '      "id": 1,\n'
        '      "text": "Question text here?",\n'
        '      "options": ["Option A", "Option B", "Option C", "Option D"],\n'
        '      "explanation": "Detailed step-by-step mathematical calculation or conceptual explanation proving why the answer is correct",\n'
        '      "answer": 2\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    if GROQ_API_KEY:
        try:
            logger.info("🤖 Querying Groq Llama 3.3 for quiz audit...")
            messages = [{"role": "user", "content": prompt}]
            response = await query_groq(messages, system_prompt=system_prompt, json_mode=True, model="llama-3.3-70b-versatile")
            if "questions" in response:
                return response
        except Exception as e:
            logger.error(f"Groq quiz audit failed: {e}")

    if GEMINI_API_KEY:
        try:
            logger.info("🤖 Querying Gemini fallback for quiz audit...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}],
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
                                        "explanation": {"type": "STRING"},
                                        "answer": {"type": "INTEGER"}
                                    },
                                    "required": ["id", "text", "options", "explanation", "answer"]
                                }
                            }
                        },
                        "required": ["questions"]
                    }
                }
            }
            timeout = aiohttp.ClientTimeout(total=180)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        text = res["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(text)
        except Exception as e:
            logger.error(f"Failed to audit quiz using Gemini fallback: {e}")

    return quiz_data

def get_mock_quiz(topic: str, count: int) -> dict:
    questions = []
    for i in range(1, count + 1):
        questions.append({
            "id": i,
            "text": f"Evaluate the basic functioning of {topic} (Question {i} of {count})?",
            "options": [
                f"Option A - Standard implementation for {topic}",
                f"Option B - Alternative parameter settings",
                f"Option C - Fallback design pattern",
                f"Option D - None of the above"
            ],
            "answer": 0
        })
    return {"questions": questions}
