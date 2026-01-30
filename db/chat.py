from db.engine import engine
from sqlalchemy import text
import json

def save_chat(thread_id, user_id, role, question, result_data):
    """
    Lưu lịch sử chat kèm theo thread_id để phục vụ hiển thị Sidebar.
    """
    # 1. Đảm bảo data là chuỗi JSON hợp lệ
    if isinstance(result_data, (dict, list)):
        json_string = json.dumps(result_data, ensure_ascii=False)
    else:
        try:
            json.loads(result_data)
            json_string = result_data
        except:
            json_string = json.dumps({"text": str(result_data)}, ensure_ascii=False)

    # 2. Thực thi INSERT vào Database
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO chat_history (thread_id, user_id, role, question, answer)
                VALUES (:t_id, :u_id, :role, :ques, :ans)
            """),
            {
                "t_id": thread_id,  # Lưu UUID phiên chat của Chainlit
                "u_id": user_id,
                "role": role,
                "ques": question,
                "ans": json_string
            },
        )