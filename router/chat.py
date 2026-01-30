from rag.index import load_index
import chainlit as cl
from rag.question_classifier import classify_question


_INDEX = None  


DOMAIN_BY_ROLE = {
    "hr": {"hr_policy"},
    "it": {"it_policy"},
    "staff": {"general"},
}


def get_index():
    global _INDEX
    if _INDEX is None:
        _INDEX = load_index()
    return _INDEX


def chat_with_rag(question: str, stream: bool = False):
    index = get_index()

    query_engine = index.as_query_engine(
        similarity_top_k=1,
        response_mode="compact",
        streaming=stream
    )

    response = query_engine.query(question)

    if stream:
        for token in response.response_gen:
            yield token
    else:
        return str(response)

from db.chat import save_chat
from db.feedback import get_rules, add_rule
from rag.retriever import retrieve_context
from llm.prompt import build_prompt
from llm.ollama_llm import call_llm, call_llm_stream
from router.schemas import SCHEMA_BY_ROLE
from router.validator import validate_and_parse



from rag.retriever import retrieve_context
from rag.question_classifier import classify_question
from llm.prompt import build_prompt
from llm.ollama_llm import call_llm
from db.feedback import get_rules





def chat_with_role(question: str, user: dict, limit: int = 5):
    role = user["role"]
    user_id = user.get("id")


    q_info = classify_question(question)

    domain = q_info.get("domain", "general")
    question_type = q_info.get("question_type", "other")
    intent = q_info.get("intent", "ask_explanation")

    print("🔎 QUESTION INFO:", q_info)


    allowed_domains = DOMAIN_BY_ROLE.get(role, set())

    if domain not in allowed_domains:
        return {
            "answer": (
                "Câu hỏi này không thuộc phạm vi xử lý "
                f"của vai trò {role.upper()}."
            ),
            "blocked": True,
            "role": role,
            "domain": domain,
            "question_type": question_type,
        }


    contexts = retrieve_context(question, role)
    context_text = "\n\n".join(contexts)

  
    rules = get_rules(role, question_type, limit)

   
    prompt = build_prompt(
        role=role,
        question=question,
        context=context_text,
        question_type=question_type,
        feedback_rules=rules,
        schema_json=None,
    )

    print("===== FINAL PROMPT =====")
    print("ROLE:", role)
    print(prompt)
    print("===== END PROMPT =====")

  
    answer_text = call_llm(prompt)

    return {
        "answer": answer_text,
        "blocked": False,
        "role": role,
        "domain": domain,
        "question_type": question_type,
        "intent": intent,
        "context_count": len(contexts),
         "question_type": question_type,
    }


    
def chat_with_role_stream(question: str, user: dict):
    role = user["role"]

    context = retrieve_context(question, role)
    rules = get_rules(role)

    prompt = build_prompt(
        role=role,
        question=question,
        context=context,
        schema_json=None,  
        feedback_rules=rules,
    )
    print("===== FINAL PROMPT =====")
    print(prompt)
    print("===== END PROMPT =====")


    for token in call_llm_stream(prompt):
        yield token
def run_chat_sync(prompt: str, user: dict):
    return chat_with_role(prompt, user)





