from src.services.quizService import generate_quiz_from_content, score_quiz_submission

async def generate_quiz(payload):
    return await generate_quiz_from_content(payload.request_id, payload.user_id)

async def submit_quiz(payload):
    return await score_quiz_submission(payload.request_id, payload.user_id, payload.answers)
