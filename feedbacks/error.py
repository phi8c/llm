ERROR_TO_POLICY = {
    # AI hiểu sai / lấy sai kiến thức
    "err_knowledge": "GENERATE_RULE",

    # AI trả lời sai vai trò / sai phạm vi
    "err_scope": "GENERATE_RULE",

    # AI suy diễn ngoài dữ liệu
    "err_hallucination": "GENERATE_RULE",

    # Lỗi không cần sinh rule
    "err_format": "IGNORE",
    "err_missing_info": "IGNORE",
}
