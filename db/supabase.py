from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url
from core.settings import Settings




def get_vector_store():
    url = make_url(Settings.SUPABASE_DB_URL)

    return PGVectorStore.from_params(
        database=url.database,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
        table_name="documents",
        embed_dim=768,
        
    )
