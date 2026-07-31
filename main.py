from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

from preprocessing.loader import DocumentLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from embeddings.embedding import EmbeddingModel
from retrieval.retriever import Retriever

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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

    context = "\n\n".join(
        chunk for _, chunk in retrieved_chunks
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                (
                    "You are a Retrieval-Augmented Generation assistant. "
                    "Answer ONLY using the provided context. "
                    "If the answer is not contained in the context say that you do not know."
                )
            },
            {
                "role": "user",
                "content":
                f"Context:\n{context}\n\nQuestion:\n{req.question}"
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return {
        "question": req.question,
        "answer": answer,
        "sources": [
            chunk for _, chunk in retrieved_chunks
        ]
    }