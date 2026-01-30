# ingest/sensitivity.py
import re
from typing import TypedDict, List


# ==============================
# OUTPUT SCHEMA
# ==============================
class SensitivityResult(TypedDict):
    suggested_access_level: str  # public | sensitive | unknown
    matched_rules: List[str]


# ==============================
# RULE DEFINITIONS
# ==============================

# Keyword nhạy cảm (HR / tài chính)
SENSITIVE_KEYWORDS = [
    "lương",
    "thu nhập",
    "thưởng",
    "đãi ngộ",
    "phúc lợi",
    "kpi",
    "hoa hồng",
    "mức đãi",
]

# Regex nhận diện số tiền / %
MONEY_PATTERNS = [
    r"\d+\s?triệu",
    r"\d+\s?%",
    r"\$\s?\d+",
    r"\d{1,3}(?:,\d{3})+",
]


# ==============================
# MAIN CLASSIFIER
# ==============================
def classify_sensitivity(chunk_text: str) -> SensitivityResult:
    """
    Rule-based sensitivity classifier.
    Không gọi LLM.
    """
    text = chunk_text.lower()
    matched = []

    # 1️⃣ Keyword match
    for kw in SENSITIVE_KEYWORDS:
        if kw in text:
            matched.append(f"keyword:{kw}")

    # 2️⃣ Money pattern match
    for pattern in MONEY_PATTERNS:
        if re.search(pattern, text):
            matched.append(f"pattern:{pattern}")

    # 3️⃣ Decision
    if matched:
        return {
            "suggested_access_level": "sensitive",
            "matched_rules": matched,
        }

    # Có thể mở rộng rule public sau
    return {
        "suggested_access_level": "public",
        "matched_rules": [],
    }
