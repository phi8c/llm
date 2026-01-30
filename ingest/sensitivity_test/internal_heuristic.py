# experiments/sensitivity_test/internal_heuristic.py

import re
from typing import Dict, List


# ==============================
# INTERNAL SIGNAL DEFINITIONS
# ==============================

# 1️⃣ Các pattern thể hiện tính CỤ THỂ (rất hay là nội bộ)
NUMERIC_PATTERNS = [
    r"\d+\s?%",                         # phần trăm
    r"\d+\s?(triệu|nghìn|tỷ|usd|\$)",   # tiền
    r"\d{4,}",                          # số lớn / mã / id
]

# 2️⃣ Từ khóa thể hiện QUY TRÌNH / NỘI BỘ
INTERNAL_KEYWORDS = [
    "nội bộ",
    "quy trình",
    "phê duyệt",
    "đánh giá",
    "báo cáo",
    "kết quả",
    "chỉ áp dụng",
    "theo quy định",
    "quản lý",
]

# 3️⃣ Dấu hiệu CẤU HÌNH / THIẾT LẬP (IT, hệ thống)
CONFIG_KEYWORDS = [
    "endpoint",
    "token",
    "api key",
    "cấu hình",
    "thiết lập",
    "tham số",
    "server",
    "database",
]

# 4️⃣ Dấu hiệu NHÂN SỰ NỘI BỘ (HR)
HR_INTERNAL_KEYWORDS = [
    "lương",
    "thưởng",
    "thu nhập",
    "kpi",
    "đãi ngộ",
    "xếp loại",
    "thăng tiến",
]


# ==============================
# MAIN HEURISTIC
# ==============================
def detect_internal(chunk_text: str) -> Dict:
    """
    Heuristic nhận diện nội dung mang tính NỘI BỘ.
    Trả về is_internal + signals để debug / review.
    """
    text = chunk_text.lower()
    signals: List[str] = []

    # 1️⃣ Numeric / concrete signals
    for pattern in NUMERIC_PATTERNS:
        if re.search(pattern, text):
            signals.append(f"pattern:{pattern}")

    # 2️⃣ Internal process keywords
    for kw in INTERNAL_KEYWORDS:
        if kw in text:
            signals.append(f"internal_kw:{kw}")

    # 3️⃣ Config / system signals
    for kw in CONFIG_KEYWORDS:
        if kw in text:
            signals.append(f"config_kw:{kw}")

    # 4️⃣ HR internal signals
    for kw in HR_INTERNAL_KEYWORDS:
        if kw in text:
            signals.append(f"hr_kw:{kw}")

    # 🔴 NGUYÊN TẮC AN TOÀN:
    # Chỉ cần CÓ 1 tín hiệu → coi là internal
    return {
        "is_internal": len(signals) > 0,
        "signals": signals,
    }
