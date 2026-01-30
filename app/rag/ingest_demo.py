from pathlib import Path
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser
from rag.index import get_index
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from db.supabase import get_vector_store
from llm.ollama_llm import load_llm


# ===== DEMO FILES CONFIG =====
DEMO_DOCS = [
    {
        "path": "data/hr.txt",
        "role_scope": "hr",
        "department": "HR",
    },
    {
        "path": "data/it.txt",
        "role_scope": "it",
        "department": "IT",
    },
    {
        "path": "data/staff.txt",
        "role_scope": "staff",
        "department": "STAFF",
    },
]

def ingest_all():
    load_llm()

    documents = []

    for cfg in DEMO_DOCS:
        text = Path(cfg["path"]).read_text(encoding="utf-8")
        documents.append(
            Document(
                text=text,
                metadata={
                    "role_scope": cfg["role_scope"],
                    "department": cfg["department"],
                }
            )
        )

    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )

    print("🎉 Ingest done with metadata persisted")
