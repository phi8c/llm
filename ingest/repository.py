# ingest/repository.py
from datetime import datetime
from sqlalchemy import text
from db.engine import engine


# =====================================================
# CHECK TRÙNG TÊN FILE
# =====================================================
def check_existing_files(file_names: list[str], role_scope: str) -> list[str]:
    """
    Trả về danh sách file_name đã tồn tại (theo role_scope)
    """
    if not file_names:
        return []

    sql = text("""
        SELECT DISTINCT metadata_->>'file_name' AS file_name
        FROM data_documents
        WHERE metadata_->>'role_scope' = :role_scope
          AND metadata_->>'file_name' = ANY(:file_names)
          AND metadata_->>'status' = 'active'
        LIMIT 10
    """)

    with engine.begin() as conn:
        rows = conn.execute(
            sql,
            {
                "role_scope": role_scope,
                "file_names": file_names,
            }
        ).fetchall()

    return [r.file_name for r in rows]


# =====================================================
# INSERT CHUNKS
# =====================================================
def insert_chunks(chunks, embeddings, metadata: dict) -> int:
    sql = text("""
        INSERT INTO data_documents (text, embedding, metadata_)
        VALUES (:text, :embedding, :metadata)
    """)

    with engine.begin() as conn:
        for i, (text_chunk, emb) in enumerate(zip(chunks, embeddings)):
            conn.execute(
                sql,
                {
                    "text": text_chunk,
                    "embedding": emb,
                    "metadata": {
                        **metadata,
                        "chunk_index": i,
                    },
                }
            )

    return len(chunks)


# =====================================================
# DEPRECATE FILE CŨ
# =====================================================
def deprecate_existing_files(file_names: list[str], role_scope: str):
    """
    Set status = deprecated cho chunk cũ (theo file_name + role_scope)
    """
    if not file_names:
        return

    now = datetime.utcnow().isoformat()

    sql = text("""
        UPDATE data_documents
        SET metadata_ = jsonb_set(
            jsonb_set(metadata_, '{status}', '"deprecated"'),
            '{deprecated_at}', to_jsonb(:deprecated_at::text)
        )
        WHERE metadata_->>'role_scope' = :role_scope
          AND metadata_->>'file_name' = ANY(:file_names)
          AND metadata_->>'status' = 'active'
    """)

    with engine.begin() as conn:
        conn.execute(
            sql,
            {
                "role_scope": role_scope,
                "file_names": file_names,
                "deprecated_at": now,
            }
        )


# =====================================================
# INSERT INGEST LOG
# =====================================================
def insert_ingest_log(
    uploaded_by: str,
    role_scope: str,
    access_level: str,
    file_count: int,
    chunk_count: int,
    status: str,
    error_message: str | None = None,
):
    sql = text("""
        INSERT INTO ingest_logs (
            uploaded_by,
            role_scope,
            access_level,
            file_count,
            chunk_count,
            status,
            error_message
        )
        VALUES (
            :uploaded_by,
            :role_scope,
            :access_level,
            :file_count,
            :chunk_count,
            :status,
            :error_message
        )
    """)

    with engine.begin() as conn:
        conn.execute(
            sql,
            {
                "uploaded_by": uploaded_by,
                "role_scope": role_scope,
                "access_level": access_level,
                "file_count": file_count,
                "chunk_count": chunk_count,
                "status": status,
                "error_message": error_message,
            }
        )
