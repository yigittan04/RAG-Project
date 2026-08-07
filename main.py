from fastapi import FastAPI
from pydantic import BaseModel
from generator.generator import Generator
from embeddings.embedding import EmbeddingModel
from retrieval.vector_store import VectorStore
from database.database import engine
from database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG")

print("Loading vector database...")

model = EmbeddingModel()

vector_store = VectorStore()

print("Ready.")


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(req: Question):

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

    return {
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