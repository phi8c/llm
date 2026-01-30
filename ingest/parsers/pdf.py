# ingest/parsers/pdf.py
from llama_index.readers.file import PDFReader


def parse_pdf(path: str) -> str:
    reader = PDFReader()
    docs = reader.load_data(path)
    return "\n".join(d.text for d in docs if d.text)
