import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL_N")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    print(">>> OLLAMA MODEL:", OLLAMA_MODEL)
    #assert Settings.OLLAMA_MODEL == "phi3:mini"

