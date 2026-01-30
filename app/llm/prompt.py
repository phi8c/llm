def build_prompt(
    role: str,
    question: str,
    context: str,
    schema_json: str,
    feedback_rules: list[str],
):
    rules = "\n".join(f"- {r}" for r in feedback_rules)

    return f"""
SYSTEM:
Bạn là trợ lý nội bộ.
Chỉ dùng thông tin được cung cấp.
Không bịa.

LUẬT BỔ SUNG:
{rules}

CONTEXT:
{context}

CÂU HỎI:
{question}

BẮT BUỘC trả lời đúng JSON schema sau:
{schema_json}

KHÔNG trả lời thêm chữ nào ngoài JSON.
"""
