
def build_prompt(
    role: str,
    question: str,
    context: str,
    question_type: str,
    schema_json: str,
    feedback_rules: list[str],
):
    role_upper = role.upper()

    return f"""
SYSTEM:
Bạn là trợ lý AI nội bộ cho vai trò {role_upper}.

LUẬT BẮT BUỘC:
- CHỈ sử dụng thông tin trong CONTEXT bên dưới.
- KHÔNG sử dụng bất kỳ kiến thức bên ngoài nào.
- Nếu CONTEXT không chứa câu trả lời, hãy trả lời:
  "Không có thông tin trong tài liệu".
- KHÔNG sinh code.
- KHÔNG suy diễn.
LUẬT BỔ SUNG:

CONTEXT (NGUỒN DUY NHẤT):
<<<
{context}
>>>

USER QUESTION:
{question}

YÊU CẦU:
- Trả lời đúng trọng tâm câu hỏi
- Trích đúng nội dung từ CONTEXT
"""



ROLE_RULES = {
    "admin": """
Bạn đang trả lời cho ADMIN.
Được phép phân tích sâu, đưa ra quyết định, đề xuất hành động.
""",
    "hr": """
Bạn đang trả lời cho NHÂN SỰ (HR).
Không tiết lộ thông tin kỹ thuật, tài chính, bảo mật.
""",
    "user": """
Bạn đang trả lời cho NGƯỜI DÙNG THƯỜNG.
Giải thích đơn giản, không dùng thuật ngữ nội bộ.
""",
}

def build_question_type_prompt(
    role: str,
    question: str,
    question_types: list[dict],
):
    types_text = "\n".join(
        f"- {t['code']}: {t['description']}"
        for t in question_types
    )

    return f"""
SYSTEM:
Bạn là hệ thống phân loại câu hỏi.

VAI TRÒ:
{role}

CÁC LOẠI CÂU HỎI HỢP LỆ:
{types_text}

CÂU HỎI:
{question}


"""


