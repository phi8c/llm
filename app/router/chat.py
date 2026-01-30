from rag.index import load_index
from parse import parse
import json

_INDEX = None  # cache global


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



def chat_with_role(question: str, user: dict, limit: int = 5 ) -> str:
    role = user["role"]
    user_id = user["id"]

    # 1. RAG theo role
    contexts = retrieve_context(question, role)
    context = "\n\n".join(contexts)

    # 2. Feedback rules (từ DB)
    rules = get_rules(role, limit)

    # 3. Build prompt (KHÔNG schema_json)
    prompt = build_prompt(
        role=role,
        question=question,
        context=context,
        schema_json=None,      # ❌ BỎ STRUCTURED OUTPUT
        feedback_rules=rules,
    )

    # 4. Call LLM → TEXT THUẦN
    
    
    #def save_chat(user_id, role, question, answer_json):
    answer_text = call_llm(prompt)
    
    parsed = json.loads(answer_text)
    

    # 5. Lưu chat (DB)
    save_chat(
    user_id=user_id,
    role=role,
    question=question,
    answer_json=answer_text,   # 👈 STRING
)

    # 6. Trả về TEXT cho Chainlit
    return {
    "answer": parsed["answer"],
    "rag_mode": parsed["use_rag"],
}

    
def chat_with_role_stream(question: str, user: dict, limit: int = 5):
    role = user["role"]

    context = retrieve_context(question, role)
    rules = get_rules(role, limit)

    prompt = build_prompt(
        role=role,
        question=question,
        context=context,
        schema_json=None,  # demo trước cho nhanh
        feedback_rules=rules,
    )

    for token in call_llm_stream(prompt):
        yield token
def run_chat_sync(prompt: str, user: dict) -> str:
    response = chat_with_role(prompt, user)
    return str(response)   # hoặc response.text




