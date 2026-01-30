# ingest/parsers/docx.py
from llama_index.readers.file import DocxReader


def parse_docx(path: str) -> str:
    reader = DocxReader()
    docs = reader.load_data(path)
    return "\n".join(d.text for d in docs if d.text)
