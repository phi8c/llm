from llm.ollama_llm import call_llm


RULE_PROMPT = """
VAI TRÒ CỦA BẠN:
Bạn KHÔNG được sáng tạo luật mới.
Bạn KHÔNG được viết quy tắc đạo đức, an toàn, giao tiếp chung chung.
Bạn chỉ được diễn đạt lại NGUYÊN TẮC SUY NGHĨ đã được hệ thống xác định.

BỐI CẢNH HỆ THỐNG:
Hệ thống đang gặp lỗi khi trả lời câu hỏi.
Hệ thống đã PHÂN LOẠI ĐƯỢC LOẠI LỖI, bạn KHÔNG cần suy đoán thêm.

THÔNG TIN ĐÃ BIẾT:
- Loại câu hỏi: {question_type}
- Nhóm lỗi: {reason}

ĐỊNH NGHĨA "RULE" TRONG HỆ THỐNG NÀY:
Rule là NGUYÊN TẮC SUY NGHĨ khi trả lời,
KHÔNG phải quy tắc đạo đức,
KHÔNG phải mô tả hệ thống,
KHÔNG phải quy trình,
KHÔNG phải checklist,
KHÔNG phải nội quy ứng xử.

RULE PHẢI:
- Chỉ áp dụng cho NHÓM câu hỏi tương ứng
- Chỉ nhằm NGĂN LỖI ĐÃ NÊU
- Điều chỉnh CÁCH SUY NGHĨ, không điều chỉnh thái độ hay văn phong

CÁC RULE MẪU ĐƯỢC PHÉP HỌC THEO (CHỈ THEO PHONG CÁCH, KHÔNG SAO CHÉP):

"Khi trả lời các câu hỏi liên quan đến chính sách, mô hình cần ưu tiên đối chiếu trực tiếp nội dung trong tài liệu chính thức thay vì suy luận từ kiến thức chung."

"Đối với các câu hỏi yêu cầu thông tin cụ thể, cần xác định rõ phạm vi và điều kiện áp dụng trước khi đưa ra câu trả lời."

"Cần tránh tổng hợp hoặc suy diễn khi tài liệu không cung cấp đầy đủ thông tin cần thiết cho câu hỏi."

YÊU CẦU OUTPUT (BẮT BUỘC):
- Chỉ viết 01 đoạn văn tiếng Việt
- Độ dài khoảng 30–50 chữ
- BẮT ĐẦU bằng một trong các cụm:
  "Khi gặp...", "Đối với...", "Cần ưu tiên..."
- KHÔNG gạch đầu dòng
- KHÔNG đánh số
- KHÔNG nhắc đến đạo đức, an toàn, bảo mật, tôn trọng, bình đẳng
- KHÔNG nhắc đến hệ thống, người dùng, AI
- KHÔNG viết chung chung áp dụng cho mọi trường hợp

Nếu bạn viết ra quy tắc mang tính đạo đức, giao tiếp chung,
hoặc không liên quan trực tiếp đến nhóm lỗi đã cho,
THÌ COI NHƯ BẠN ĐÃ TRẢ LỜI SAI.

OUTPUT (CHỈ VIẾT NỘI DUNG RULE):


"""


def generate_rule(question, answer, reason, question_type):
    
    prompt = RULE_PROMPT.format(
        question=question,
        answer=answer,
        reason=reason,
        question_type=question_type,
    )
    return call_llm(prompt).strip()
