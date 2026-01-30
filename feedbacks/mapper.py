from typing import TypedDict

class ErrorSemantic(TypedDict):
    label: str          # Tên lỗi, cho log / UI
    description: str    # Mô tả lỗi (cho hệ thống hiểu)
    category: str       # Dùng để map sang rule_type
    llm_hint: str       # HƯỚNG DẪN CỨNG cho LLM





def map_feedback_to_error_type(
    feedback_level_1: str,
    feedback_level_2: str | None = None,
) -> str:
    """
    Map feedback của user thành error_type nội bộ.
    Trả về 1 trong các error_type chuẩn.
    """

    # ----- Level 1 -----
    if feedback_level_1 == "F1":  # Lấy sai kiến thức
        if feedback_level_2 == "F1.1":
            return "err_scope"           # sai lĩnh vực / domain
        if feedback_level_2 == "F1.2":
            return "err_knowledge"       # sai loại chính sách
        if feedback_level_2 == "F1.3":
            return "err_knowledge"       # không rõ nguồn
        return "err_knowledge"

    if feedback_level_1 == "F2":          # Thiếu thông tin
        return "err_missing_info"

    if feedback_level_1 == "F3":          # Suy diễn
        return "err_hallucination"

    if feedback_level_1 == "F4":          # Trình bày
        return "err_format"

    if feedback_level_1 == "F5":          # Không đúng trọng tâm
        return "err_scope"

    # fallback an toàn
    return "err_format"

ERROR_SEMANTIC_MAP = {
    "err_scope": "Câu trả lời sai phạm vi câu hỏi (lấy sai lĩnh vực hoặc trả lời lệch trọng tâm).",

    "err_knowledge": "Câu trả lời sử dụng hoặc diễn giải sai kiến thức chính sách so với câu hỏi.",

    "err_missing_info": "Câu trả lời chưa cung cấp đủ thông tin cần thiết.",

    "err_hallucination": "Câu trả lời có nội dung suy diễn, không có căn cứ từ tài liệu.",

    "err_format": "Câu trả lời có vấn đề về cách trình bày hoặc cấu trúc."
}

def map_error_type_to_semantic(error_type: str) -> str:
    return ERROR_SEMANTIC_MAP.get(
        error_type,
        "Câu trả lời có lỗi nhưng không xác định được loại lỗi cụ thể."
    )



