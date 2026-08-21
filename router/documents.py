from uuid import UUID
from preprocessing.loader import DocumentLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from embeddings.embedding import EmbeddingModel
from retrieval.store import vector_store

import hashlib
import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.database import get_db
from database import crud


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = "uploads"

embedding_model = EmbeddingModel()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    file_data = await file.read()

    if not file_data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    file_hash = hashlib.sha256(
        file_data
    ).hexdigest()

    existing_document = crud.get_document_by_hash(
        db=db,
        file_hash=file_hash
    )

    if existing_document is not None:
        raise HTTPException(
            status_code=409,
            detail="This document has already been uploaded."
        )

    document_id = uuid.uuid4()

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    storage_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}{extension}"
    )

    with open(storage_path, "wb") as f:
        f.write(file_data)

    uploaded_by = os.getenv("INDEX_USER_ID")

    if not uploaded_by:
        raise HTTPException(
            status_code=500,
            detail="INDEX_USER_ID environment variable is not configured."
        )

    document = crud.create_document(
        db=db,
        filename=file.filename,
        uploaded_by=uploaded_by,
        total_chunks=0,
        file_size=len(file_data),
        mime_type=file.content_type or "application/octet-stream",
        storage_path=storage_path,
        file_hash=file_hash,
        status="processing"
    )

    try:

        text = DocumentLoader.load(
            storage_path
        )

        clean_text = TextCleaner.clean(
            text
        )

        chunks = TextChunker.chunk_by_paragraph(
            clean_text
        )

        if not chunks:
            raise ValueError(
                "No text could be extracted from the document."
            )

        chunk_records = []

        for i, chunk_text in enumerate(chunks):

            chunk = crud.create_chunk(
                db=db,
                document_id=document.id,
                chunk_index=i,
                page_number=None,
                content=chunk_text
            )

            chunk_records.append(chunk)

        chunk_embeddings = embedding_model.embed_documents(
            chunks
        )

        metadata = [
            {
                "chunk_id": str(chunk.id),
                "document_id": str(document.id),
                "content": chunk.content
            }
            for chunk in chunk_records
        ]

        vector_store.add_chunks(
            embeddings=chunk_embeddings,
            metadata=metadata
        )

        vector_store.save()

        crud.update_document_status(
            db=db,
            document_id=document.id,
            status="processed"
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Failed to process document."
        )

    return {
        "document_id": str(document.id),
        "filename": document.filename,
        "status": document.status,
        "chunk_count": len(chunk_records)
    }

@router.get("")
def get_documents(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    documents = crud.get_documents(
        db=db,
        user_id=user_id
    )

    return documents

@router.get("/{document_id}")
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db)
):
    document = crud.get_document(
        db=db,
        document_id=document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return document