from uuid import UUID
from preprocessing.loader import DocumentLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from embeddings.embedding import EmbeddingModel
from retrieval.store import vector_store
from database.models import User
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
from security import get_current_user

import hashlib
import os
import uuid
import logging


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"

embedding_model = EmbeddingModel()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    uploaded_by = current_user.id

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

    faiss_modified = False

    try:

        with open(storage_path, "wb") as f:
            f.write(file_data)

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
                "content": chunk.content,
                "embedding": embedding
            }
            for chunk, embedding in zip(
                chunk_records,
                chunk_embeddings
            )
        ]

        vector_store.add_chunks(
            embeddings=chunk_embeddings,
            metadata=metadata
        )

        faiss_modified = True

        vector_store.save()

        document.total_chunks = len(chunk_records)

        crud.update_document_status(
            db=db,
            document_id=document.id,
            status="processed"
        )

        db.commit()

        db.refresh(document)

    except Exception as e:

        logger.exception("Failed to upload document %s", document.id)

        db.rollback()

        if faiss_modified:
            try:
                deleted = vector_store.delete_document(
                    document_id=document_id
                )

                if deleted:
                    vector_store.save()
                
            except Exception:

                logger.exception("Failed to rollback FAISS for document %s", document_id)

        try:

            if os.path.exists(storage_path):
                os.remove(storage_path)

        except Exception:

            logger.exception("Failed to delete uploaded file %s", storage_path)

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = crud.get_documents(
        db=db,
        user_id=current_user.id
    )

    return documents

@router.get("/{document_id}")
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    if document.uploaded_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this document."
        )    

    return document

@router.delete("/{document_id}")
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    if document.uploaded_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this document."
        )

    try:

        if document.storage_path and os.path.exists(
            document.storage_path
        ):
            os.remove(document.storage_path)

        deleted = vector_store.delete_document(
            document_id=document_id
        )

        if deleted:
            vector_store.save()

        crud.delete_document(
            db=db,
            document_id=document_id
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete document."
        )

    return {
        "message": "Document deleted successfully.",
        "document_id": str(document_id)
    }