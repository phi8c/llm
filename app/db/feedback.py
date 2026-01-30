from sqlalchemy import text
from db.engine import engine


def get_rules(role: str, limit: int = 3) -> list[str]:
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
            SELECT rule
            FROM feedback_rules
            WHERE role = :r
            ORDER BY created_at DESC
            LIMIT :limit
            """),
            {"r": role, "limit": limit},
        ).fetchall()

    return [r[0] for r in rows]



def add_rule(role: str, rule: str):
    with engine.begin() as conn:
        # kiểm tra rule đã tồn tại chưa
        exists = conn.execute(
            text("""
            SELECT 1 FROM feedback_rules
            WHERE role = :r AND rule = :rule
            """),
            {"r": role, "rule": rule},
        ).fetchone()

        if exists:
            return  # đã có rồi thì thôi

        conn.execute(
            text("""
            INSERT INTO feedback_rules (role, rule)
            VALUES (:r, :rule)
            """),
            {"r": role, "rule": rule},
        )
