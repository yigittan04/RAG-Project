from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID
from sqlalchemy.orm import Session
from generator.generator import Generator
from embeddings.embedding import EmbeddingModel
from retrieval.store import vector_store
from database.database import engine, get_db
from database.models import Base, User
from database import crud
from generation.prompt_builder import PromptBuilder
from router.conversations import router as conversations_router
from router.documents import router as documents_router
from router.auth import router as auth_router
from security import get_current_user

import time


app = FastAPI(title="RAG")

app.include_router(conversations_router)
app.include_router(documents_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

print("Loading vector database...")

model = EmbeddingModel()

print("Ready.")


class Question(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )
    conversation_id: UUID | None = None
    document_id: UUID | None = None


@app.post("/ask")
def ask(
    req: Question,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if req.conversation_id:

        conversation = crud.get_conversation(
            db=db,
            conversation_id=req.conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found."
            )

        if conversation.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this conversation."
            )

    else:

        conversation = crud.create_conversation(
            db=db,
            user_id=current_user.id,
            title=req.question[:50]
        )

    if req.document_id:

        document = crud.get_document(
            db=db,
            document_id=req.document_id
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

    previous_messages = crud.get_messages(
        db=db,
        conversation_id=conversation.id
    )

    user_message = crud.create_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=req.question
    )

    question_embedding = model.embed(
        req.question
    )

    retrieval_start = time.perf_counter()

    retrieved_chunks = vector_store.search(
        question_embedding,
        top_k=3,
        document_id=req.document_id
    )

    retrieval_latency = (
        time.perf_counter() - retrieval_start
    ) * 1000

    for rank, result in enumerate(
        retrieved_chunks,
        start=1
    ):

        crud.create_retrieval_log(
            db=db,
            message_id=user_message.id,
            chunk_id=result["chunk_id"],
            similarity=result["similarity"],
            latency_ms=retrieval_latency,
            rank=rank
        )

    context_chunks = [
        result["content"]
        for result in retrieved_chunks
    ]

    prompt = PromptBuilder.build(
        context_chunks=context_chunks,
        question=req.question,
        conversation_history=previous_messages
    )

    answer = Generator.answer(
        prompt
    )

    assistant_message = crud.create_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=answer
    )

    return {
        "conversation_id": str(conversation.id),
        "user_message_id": str(user_message.id),
        "assistant_message_id": str(assistant_message.id),
        "question": req.question,
        "answer": answer,
        "sources": [
            result["content"]
            for result in retrieved_chunks
        ]
    }