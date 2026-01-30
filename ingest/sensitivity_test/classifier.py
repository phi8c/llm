def classify(text: str) -> str:
    t = text.lower()

    if any(k in t for k in ["lương", "thưởng", "thu nhập"]):
        return "compensation"

    if any(k in t for k in ["hợp đồng", "ký kết"]):
        return "contract"

    if any(k in t for k in ["kiến trúc", "microservice", "kubernetes"]):
        return "architecture"

    if any(k in t for k in ["bảo mật", "security"]):
        return "security"

    if any(k in t for k in ["test", "kiểm thử", "hiệu năng"]):
        return "test_result"

    return "general"
