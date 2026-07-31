from fastapi import FastAPI
from pydantic import BaseModel

from preprocessing.loader import DocumentLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from embeddings.embedding import EmbeddingModel
from retrieval.retriever import Retriever

app = FastAPI(title="RAG")

print("Loading documents...")

text = DocumentLoader.load("data/test.txt")

clean_text = TextCleaner.clean(text)

chunks = TextChunker.chunk_by_paragraph(clean_text)

model = EmbeddingModel()

embeddings = model.embed_documents(chunks)

print("Ready.")

class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(req: Question):

    question_embedding = model.embed(req.question)

    retrieved_chunks = Retriever.retrieve(
        question_embedding,
        embeddings,
        chunks,
        top_k=3
    )

    results = []

    for score, chunk in retrieved_chunks:
        results.append({
            "similarity": float(score),
            "text": chunk
        })

    return {
        "question": req.question,
        "results": results
    }