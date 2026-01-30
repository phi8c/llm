from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from db.supabase import get_vector_store
from llm.ollama_llm import load_llm

from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex


BASE_DIR = Path(__file__).resolve().parents[1]  # trỏ tới app/
DATA_DIR = BASE_DIR.parent / "data"             # trỏ tới data/

def build_index():
    load_llm()  # 👈 BẮT BUỘC

    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )

def load_index():
    vector_store = get_vector_store()
    return VectorStoreIndex.from_vector_store(vector_store)


# app/rag/index.py
# app/rag/index.py
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from db.supabase import get_vector_store

_index = None

def get_index():
    global _index
    if _index is None:
        # 🔹 SET EMBEDDING = OLLAMA (KHÔNG OPENAI)
        Settings.embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            base_url="http://localhost:11434",
        )

        vector_store = get_vector_store()
        _index = VectorStoreIndex.from_vector_store(vector_store)

    return _index


