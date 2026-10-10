import ast
import json
from app.database.core import connect
from app.database.persistence import initialize_persistence_database
from app.rag.embeddings import cosine_similarity, embed_text


def search(query: str, limit: int = 5) -> list[dict]:
    initialize_persistence_database()
    query_embedding = embed_text(query)
    with connect() as connection:
        rows = connection.execute(
            "SELECT id, title, source_url, publisher, published_at, reliability, content, embedding_json FROM rag_documents"
        ).fetchall()
    results = []
    for row in rows:
        try:
            embedding = json.loads(row["embedding_json"])
        except (TypeError, json.JSONDecodeError):
            embedding = ast.literal_eval(row["embedding_json"])
        score = cosine_similarity(query_embedding, embedding) * float(row["reliability"])
        results.append({
            "id": row["id"], "title": row["title"], "url": row["source_url"],
            "publisher": row["publisher"], "published_at": row["published_at"],
            "content": row["content"], "score": round(score, 4),
        })
    return sorted(results, key=lambda item: item["score"], reverse=True)[:limit]
