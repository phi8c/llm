from llm.ollama_llm import call_llm
from llm.prompt import build_question_type_prompt
from db.feedback import get_question_types_by_role


def classify_question(role: str, question: str) -> str | None:
    question_types = get_question_types_by_role(role)

    if not question_types:
        return None

    prompt = build_question_type_prompt(
        role=role,
        question=question,
        question_types=question_types,
    )

    result = call_llm(prompt).strip().lower()

    valid_codes = {t["code"] for t in question_types}
    if result not in valid_codes:
        return None

    return result
