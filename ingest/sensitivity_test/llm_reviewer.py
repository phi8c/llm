# experiments/sensitivity_test/llm_reviewer.py

import sys
from pathlib import Path

# Add project root to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from typing import Literal
from constants import SENSITIVITY_TAGS
from llm.ollama_llm import call_llm


SensitivityTag = Literal[
    "compensation",
    "contract",
    "architecture",
    "security",
    "test_result",
    "general",
    "unknown",
]


PROMPT_TEMPLATE = """
Bạn là hệ thống phân loại dữ liệu nội bộ.

NHIỆM VỤ:
Phân loại đoạn văn xem đoạn văn đó có thuộc loại nhạy cảm hay không
Đoạn văn nhạy cảm nghĩa là nó có nhắc tới số tiền, tài sản, thông tin bí mật trong một công ty
Nếu thông tin đó là nhạy cảm thì hãy phân nó là sensitive và trả về nhãn sensitive

QUY TẮC BẮT BUỘC:
- Chỉ trả về DUY NHẤT tên nhãn.
- Không giải thích.
- Không viết câu hoàn chỉnh.
- Không thêm ký tự thừa.

ĐOẠN VĂN:
{chunk_text}
""".strip()


def normalize_output(text: str) -> str:
    """
    Chuẩn hóa output của LLM để tránh lỗi format nhẹ.
    """
    if not text:
        return "unknown"

    t = text.strip().lower()

    # Chỉ lấy dòng đầu tiên nếu model xuống dòng
    t = t.splitlines()[0].strip()

    # Lọc nếu model trả linh tinh
    if t not in SENSITIVITY_TAGS:
        return "unknown"

    return t


def review_with_llm(chunk_text: str) -> SensitivityTag:
    """
    Gọi LLM để review sensitivity tag.
    Không auto-apply, chỉ dùng để so sánh / gợi ý.
    """
    prompt = PROMPT_TEMPLATE.format(chunk_text=chunk_text)

    try:
        raw = call_llm(prompt)
        print("in ra raw của model", raw)
        tag = normalize_output(raw)
        return tag
    except Exception as e:
        print("⚠️ LLM reviewer error:", e)
        return "unknown"
