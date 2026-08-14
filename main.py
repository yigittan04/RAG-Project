from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from generator.generator import Generator
from embeddings.embedding import EmbeddingModel
from retrieval.vector_store import VectorStore
from database.database import engine, get_db
from database.models import Base
from database import crud


Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG")

print("Loading vector database...")

model = EmbeddingModel()
vector_store = VectorStore()

print("Ready.")


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(
    req: Question,
    db: Session = Depends(get_db)
):

    conversation = crud.create_conversation(
        db=db,
        title=req.question[:50]
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

    context = "\n\n".join(
        chunk for _, chunk in retrieved_chunks
    )

    answer = Generator.answer(
        req.question,
        context
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
            chunk for _, chunk in retrieved_chunks
        ]
    }

@app.get("/")
def root():
    return {
        "message": "RAG API is running.",
        "docs": "/docs"
    }