# db/users.py
from db.config import supabase 

def get_user_role(user_id):
    try:
        # Dùng SDK (Port 443) thay vì SQLAlchemy (Port 6543)
        res = supabase.table("users").select("role").eq("id", user_id).execute()
        
        if res.data:
            return res.data[0].get("role", "user")
        return "user"
    except Exception as e:
        print(f"--- [ROLE ERROR] {e} ---")
        return "user"