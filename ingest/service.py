# ingest/service.py
from ingest.parsers.pdf import parse_pdf
from ingest.parsers.docx import parse_docx
from ingest.parsers.txt import parse_txt
from ingest.parsers.csv import parse_csv
from ingest.chunker import chunk_text
from ingest.embedder import embed_texts
from ingest.repository import insert_chunks, check_existing_files, deprecate_existing_files, insert_ingest_log


def _parse_file(file):
    name = file.name.lower()
    path = file.path

    if name.endswith(".pdf"):
        return parse_pdf(path)
    if name.endswith(".docx"):
        return parse_docx(path)
    if name.endswith(".txt"):
        return parse_txt(path)
    if name.endswith(".csv"):
        return parse_csv(path)

    return ""


async def ingest_files(
    files,
    role_scope: str,
    uploaded_by: str,
    access_level: str,
):
    total_chunks = 0
    file_names = [f.name for f in files]

    try:
        # 1️⃣ DEPRECATE FILE CŨ (NẾU CÓ)
        deprecate_existing_files(
            file_names=file_names,
            role_scope=role_scope,
        )

        # 2️⃣ INGEST FILE MỚI
        for file in files:
            text = _parse_file(file)
            if not text.strip():
                continue

            chunks = chunk_text(text)
            embeddings = embed_texts(chunks)

            metadata = {
                "role_scope": role_scope,
                "file_name": file.name,
                "uploaded_by": uploaded_by,
                "status": "active",
                "access_level": access_level,
            }

            total_chunks += insert_chunks(chunks, embeddings, metadata)

        # 3️⃣ LOG SUCCESS
        insert_ingest_log(
            uploaded_by=uploaded_by,
            role_scope=role_scope,
            access_level=access_level,
            file_count=len(files),
            chunk_count=total_chunks,
            status="success",
        )

        return {
            "files": len(files),
            "chunks": total_chunks,
        }

    except Exception as e:
        # 🔴 LOG FAILED
        insert_ingest_log(
            uploaded_by=uploaded_by,
            role_scope=role_scope,
            access_level=access_level,
            file_count=len(files),
            chunk_count=total_chunks,
            status="failed",
            error_message=str(e),
        )
        raise


# ingest/service.py

def precheck_files(files, role_scope: str):
    file_names = [f.name for f in files]
    duplicated = check_existing_files(file_names, role_scope)

    return {
        "has_duplicate": bool(duplicated),
        "duplicated_files": duplicated,
    }

