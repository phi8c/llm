# app/db/users.py
from sqlalchemy import text
from db.engine import engine


def get_user_role(user_id: str) -> str | None:
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT role FROM users WHERE id = :id"),
            {"id": user_id},
        ).fetchone()

    return row[0] if row else None
