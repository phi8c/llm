from sqlalchemy import text
from db.engine import engine




def get_rules(role: str, question_type: str, limit: int = 5) -> list[str]:
    """
    Lấy các rule GLOBAL đang active cho 1 role.
    Dùng để inject vào prompt.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
            SELECT rule
            FROM feedback_rules
            WHERE 
               role = :role
              AND question_type = :question_type
            ORDER BY created_at DESC
            LIMIT :limit
            """),
            {
                "role": role,
                "limit": limit,
                "question_type": question_type
            },
        ).fetchall()

    return [r[0] for r in rows]


def add_rule(
    role: str,
    rule: str,
    rule_type: str | None = None,
    question_type: str | None = None,
):
    """
    Thêm rule GLOBAL mới.
    - Không lưu trùng nội dung
    - Chuẩn bị cho việc ghi đè theo rule_type
    """

    with engine.begin() as conn:
      
        exists = conn.execute(
            text("""
            SELECT 1
            FROM feedback_rules
            WHERE user_id IS NULL
              AND role = :role
              AND LOWER(rule) = LOWER(:rule)
            """),
            {
                "role": role,
                "rule": rule,
            },
        ).fetchone()

        if exists:
            return

      
        if rule_type:
            conn.execute(
                text("""
                UPDATE feedback_rules
                SET is_active = false
                WHERE user_id IS NULL
                  AND role = :role
                  AND rule_type = :rule_type
                """),
                {
                    "role": role,
                    "rule_type": rule_type,
                },
            )

       
        conn.execute(
            text("""
            INSERT INTO feedback_rules (
                user_id,
                role,
                rule,
                rule_type,
                question_type,
                is_active
            )
            VALUES (
                NULL,
                :role,
                :rule,
                :rule_type,
                :question_type,
                true
            )
            """),
            {
                "role": role,
                "rule": rule,
                "rule_type": rule_type,
                "question_type": question_type,
            },
        )




def get_question_types_by_role(role: str) -> list[dict]:
    """
    Lấy danh sách loại câu hỏi hợp lệ cho 1 role.
    Đây là bảng dictionary, không phải log.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
            SELECT code, description
            FROM question_types
            WHERE role = :role
              AND is_active = true
            ORDER BY code
            """),
            {"role": role},
        ).fetchall()

    return [
        {
            "code": r[0],
            "description": r[1],
        }
        for r in rows
    ]
