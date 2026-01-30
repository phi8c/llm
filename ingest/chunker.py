# ingest/chunker.py
from llama_index.core.node_parser import SentenceSplitter


def chunk_text(text: str, chunk_size=400, overlap=50):
    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    return splitter.split_text(text)
