from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user
from app.rag.ingest import ingest_document
from app.rag.retrieval import search

router = APIRouter(prefix="/rag", tags=["RAG"])


class DocumentRequest(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1, max_length=200_000)
    source_url: str | None = None
    publisher: str | None = None
    published_at: str | None = None
    reliability: float = Field(default=0.5, ge=0, le=1)


@router.post("/documents")
def add_document(request: DocumentRequest, _: dict[str, str] = Depends(get_current_user)):
    document_id = ingest_document(**request.model_dump())
    return {"id": document_id}


@router.get("/search")
def retrieve_documents(query: str, limit: int = 5, _: dict[str, str] = Depends(get_current_user)):
    return {"sources": search(query, max(1, min(limit, 20)))}
