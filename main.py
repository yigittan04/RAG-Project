from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from generator.generator import Generator
from embeddings.embedding import EmbeddingModel
from retrieval.vector_store import VectorStore
from database.database import engine, get_db
from database.models import Base
from database import crud
from generation.prompt_builder import PromptBuilder

import time


Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG")

print("Loading vector database...")

model = EmbeddingModel()
vector_store = VectorStore()

print("Ready.")


class Question(BaseModel):
    question: str
    conversation_id: str | None = None


@app.post("/ask")
def ask(
    req: Question,
    db: Session = Depends(get_db)
):

    if req.conversation_id:
        conversation = crud.get_conversation(
            db=db,
            conversation_id=req.conversation_id
        )

        if conversation is None:
            return {
                "error": "Conversation not found."
            }
    else:
        conversation = crud.create_conversation(
        db=db,
        title=req.question[:50]
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

    question_embedding = model.embed(req.question)

    retrieved_chunks = vector_store.search(
        question_embedding,
        top_k=3
    )

    retrieval_start = time.perf_counter()

    retrieved_chunks = vector_store.search(
        question_embedding,
        top_k=3
    )

    retrieval_latency = (
        time.perf_counter() - retrieval_start
    ) * 1000

    for rank, (similarity, chunk) in enumerate(
    retrieved_chunks,
    start=1
    ):
        chunk_record = (
            db.query(crud.Chunk)
            .filter(crud.Chunk.content == chunk)
            .first()
        )

        if chunk_record:
            crud.create_retrieval_log(
                db=db,
                message_id=user_message.id,
                chunk_id=chunk_record.id,
                similarity=similarity,
                latency_ms=retrieval_latency,
                rank=rank
            )

    context_chunks = [
        chunk for _, chunk in retrieved_chunks
    ]

    prompt = PromptBuilder.build(
        context_chunks=context_chunks,
        question=req.question,
        conversation_history=previous_messages
    )

    answer = Generator.answer(prompt)

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
            chunk for _, chunk in retrieved_chunks
        ]
    }

@app.get("/")
def root():
    return {
        "message": "RAG API is running.",
        "docs": "/docs"
    }