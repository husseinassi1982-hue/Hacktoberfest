import json
import re
from datetime import datetime, timezone

from app.database.core import connect
from app.database.persistence import initialize_persistence_database
from app.rag.embeddings import embed_text


def clean_text(content: str) -> str:
    return re.sub(r"\s+", " ", content).strip()


def chunk_text(content: str, chunk_size: int = 1200, overlap: int = 150) -> list[str]:
    content = clean_text(content)
    if not content:
        return []
    chunks = []
    start = 0
    while start < len(content):
        end = min(len(content), start + chunk_size)
        chunks.append(content[start:end])
        if end == len(content):
            break
        start = end - overlap
    return chunks


def ingest_document(*, title: str, content: str, source_url: str | None = None,
                    publisher: str | None = None, published_at: str | None = None,
                    reliability: float = 0.5) -> int:
    initialize_persistence_database()
    chunks = chunk_text(content)
    if not chunks:
        raise ValueError("Document content cannot be empty.")
    now = datetime.now(timezone.utc).isoformat()
    with connect() as connection:
        cursor = connection.execute(
            "INSERT INTO rag_documents(title, source_url, publisher, published_at, reliability, content, embedding_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id",
            (title, source_url, publisher, published_at, reliability, chunks[0], json.dumps(embed_text(chunks[0])), now),
        )
        document_id = cursor.fetchone()["id"]
        for chunk in chunks[1:]:
            connection.execute(
                "INSERT INTO rag_documents(title, source_url, publisher, published_at, reliability, content, embedding_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title, source_url, publisher, published_at, reliability, chunk, json.dumps(embed_text(chunk)), now),
            )
    return int(document_id)
