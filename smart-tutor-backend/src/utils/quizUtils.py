import random
from transformers import pipeline

qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-base-qg-hl")

def extract_candidate_answers(text: str, count: int = 10):
    words = list(set(text.split()))
    return random.sample(words, min(count, len(words)))

def generate_question(context: str, answer: str) -> str:
    hl_context = context.replace(answer, f"<hl> {answer} <hl>")
    prompt = f"generate question: {hl_context}"
    result = qg_pipeline(prompt, max_length=64, do_sample=False)[0]["generated_text"]
    return result

def generate_distractors(answer: str, corpus_words: list, k: int = 3):
    distractors = [w for w in corpus_words if w.lower() != answer.lower()]
    return random.sample(distractors, min(k, len(distractors)))

def build_question_payload(context: str, answer: str, qid: str, corpus_words: list):
    question = generate_question(context, answer)
    options = generate_distractors(answer, corpus_words) + [answer]
    random.shuffle(options)
    return {
        "id": qid,
        "question": question,
        "options": options,
        "answer": answer
    }
