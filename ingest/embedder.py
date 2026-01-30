# ingest/embedder.py
from llama_index.embeddings.ollama import OllamaEmbedding


_embedding = None


def get_embedder():
    global _embedding
    if _embedding is None:
        _embedding = OllamaEmbedding(model_name="nomic-embed-text")
    return _embedding


def embed_texts(texts: list[str]) -> list[list[float]]:
    embedder = get_embedder()
    return [embedder.get_text_embedding(t) for t in texts]
