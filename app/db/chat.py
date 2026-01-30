from db.engine import engine
from sqlalchemy import text


def save_chat(user_id, role, question, answer_json):
    with engine.begin() as conn:
        conn.execute(
            text("""
            insert into chat_history (user_id, role, question, answer)
            values (:i, :r, :q, :a)
            """),
            {
                "i": user_id,
                "r": role,
                "q": question,
                "a": answer_json,
            },
        )
