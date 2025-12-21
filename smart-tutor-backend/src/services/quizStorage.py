import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def save_quiz(request_id, user_id, quiz):
    key = f"quiz:{user_id}:{request_id}"
    r.set(key, json.dumps(quiz))

async def get_quiz(request_id, user_id):
    key = f"quiz:{user_id}:{request_id}"
    data = r.get(key)
    return json.loads(data) if data else None

async def save_quiz_result(user_id, request_id, result):
    key = f"quiz_result:{user_id}:{request_id}"
    r.set(key, json.dumps(result))
