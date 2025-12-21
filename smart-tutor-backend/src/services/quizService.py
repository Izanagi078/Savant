from src.services.quizStorage import save_quiz, get_quiz, save_quiz_result
from src.services.redisService import get_content
from src.utils.quizUtils import extract_candidate_answers, build_question_payload

async def generate_quiz_from_content(request_id: str, user_id: str):
    data = await get_content(request_id)
    if not data or "resources" not in data:
        raise ValueError("No content found")

    topic = data.get("topic", "unknown")
    texts = [r.get("summary") or r.get("snippet") for r in data["resources"] if r.get("source") in {"Web", "PDF"}]
    combined_text = "\n".join(filter(None, texts))
    corpus_words = list(set(combined_text.split()))

    answers = extract_candidate_answers(combined_text)
    questions = [
        build_question_payload(combined_text, ans, f"q{i+1}", corpus_words)
        for i, ans in enumerate(answers)
    ]

    quiz = {
        "request_id": request_id,
        "user_id": user_id,
        "topic": topic,
        "questions": questions
    }

    await save_quiz(request_id, user_id, quiz)
    return quiz

async def score_quiz_submission(request_id: str, user_id: str, answers: dict):
    quiz = await get_quiz(request_id, user_id)
    if not quiz:
        raise ValueError("Quiz not found")

    correct_answers = {}
    score = 0
    for q in quiz["questions"]:
        qid = q["id"]
        correct = q["answer"]
        user_ans = answers.get(qid)
        is_correct = user_ans == correct
        correct_answers[qid] = is_correct
        if is_correct:
            score += 1

    result = {
        "user_id": user_id,
        "request_id": request_id,
        "topic": quiz["topic"],
        "score": score,
        "total": len(quiz["questions"]),
        "correct_answers": correct_answers
    }

    await save_quiz_result(user_id, request_id, result)
    return {
        "score": score,
        "total": len(quiz["questions"]),
        "correct_answers": correct_answers
    }
