# RAG Project

Retrieval-Augmented Generation application built with FastAPI, FAISS, Jina AI Embeddings, and the Groq API.

The application retrieves the most relevant information from a collection of documents using semantic vector search and generates context aware answers with a LLM.

---

# How It Works

1. Documents are loaded and cleaned.
2. Documents are split into smaller chunks.
3. Each chunk is converted into a vector embedding using the Jina Embeddings API.
4. Embeddings are stored inside a FAISS vector database.
5. When a user asks a question:
   - The question is converted into an embedding.
   - FAISS retrieves the most semantically similar document chunks.
   - The retrieved context is sent to a Groq-hosted Llama model.
   - The model generates an answer using only the retrieved context.

The API also returns the document chunks that were used to generate the response.

---

# Features

- RAG
- Semantic document search
- FAISS vector database
- Context aware answer generation
- Source document retrieval
- REST API built with FastAPI
- Automatic Swagger/OpenAPI documentation
- Deployable on Render

---

# Technologies

## Backend

- FastAPI
- Pydantic
- Uvicorn

## Retrieval

- FAISS
- NumPy

## Embeddings

- Jina AI Embeddings API

## LLM

- Groq API
- Llama 3.3 70B Versatile

## Document Processing

- PyMuPDF
- python-docx

## Deployment

- Render

---

# Project Structure

```
rag_project/
│
├── data/
├── database/
├── embeddings/
├── generation/
├── generator/
├── preprocessing/
├── prompts/
├── retrieval/
├── utils/
│
├── app.py
├── index.py
├── main.py
├── config.py
└── requirements.txt
```

---

# API

## POST `/ask`

Accepts a natural language question.

Example request:

```json
{
  "question": "What is Python?"
}
```

Example response:

```json
{
  "question": "What is Python?",
  "answer": "Python is a programming language.",
  "sources": [
    "Python is a programming language."
  ]
}
```
