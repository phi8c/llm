import json
from llm.ollama_llm import call_llm


CLASSIFY_PROMPT = """
Bạn là hệ thống phân loại câu hỏi cho trợ lý nội bộ của doanh nghiệp.

Hãy phân tích CÂU HỎI và trả về KẾT QUẢ PHÂN LOẠI theo ĐÚNG định dạng JSON.
câu hỏi: {question} thuộc lĩnh vực nào dưới đây:

- hr_policy        : chính sách / quy định nhân sự
- it_policy        : quy định trong lĩnh vực IT, công nghệ thông tin
- finance_policy   : chính sách / quy định tài chính
- general          : câu hỏi chung, không thuộc chính sách cụ thể

YÊU CẦU:
- KHÔNG giải thích
- KHÔNG thêm chữ
- CHỈ trả về JSON hợp lệ

CÁC TRƯỜNG CẦN TRẢ VỀ:

1. domain (lĩnh vực câu hỏi), chỉ chọn 1 trong các giá trị:
- hr_policy        : chính sách / quy định nhân sự
- it_policy        : quy định trong lĩnh vực IT, công nghệ thông tin
- finance_policy   : chính sách / quy định tài chính
- general          : câu hỏi chung, không thuộc chính sách cụ thể

2. question_type (loại câu hỏi), chỉ chọn 1 trong:
- policy       : hỏi về quy định, chính sách
- procedure    : hỏi về quy trình, các bước thực hiện
- definition   : hỏi định nghĩa, khái niệm
- how_to       : hỏi cách làm
- yes_no       : câu hỏi có/không
- other        : loại khác

3. intent (mục đích câu hỏi), chỉ chọn 1 trong:
- ask_rule          : hỏi nội dung quy định
- ask_process       : hỏi quy trình thực hiện
- ask_explanation   : hỏi giải thích
- ask_confirmation  : hỏi xác nhận đúng/sai

CHỈ TRẢ VỀ JSON.
""".strip()



def classify_question(question: str) -> dict:
    response = call_llm(
        CLASSIFY_PROMPT.format(question=question)
    )

    try:
        result = json.loads(response)
    except Exception:
        # fallback an toàn
        result = {
            "domain": "general",
            "question_type": "other",
            "intent": "ask_explanation",
        }

    return result
