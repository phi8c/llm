import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.environ.get("SUPABASE_PROJECT_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

# Khởi tạo client ở đây để dùng chung cho toàn bộ dự án
supabase: Client = create_client(supabase_url, supabase_key)