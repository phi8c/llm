from sqlalchemy import create_engine
from core.settings import Settings

engine = create_engine(
    Settings.SUPABASE_DB_URL,
    pool_pre_ping=True,
)
