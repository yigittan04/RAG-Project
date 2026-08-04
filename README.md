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

---

# Deployment

## Live Application

https://rag-project-icjj.onrender.com

Swagger / OpenAPI Documentation:

https://rag-project-icjj.onrender.com/docs

---

## Render Service

- Backend: Render Web Service
- Database: FAISS vector database

---

## Environment Variables

These environment variables are required:

```
GROQ_API_KEY
JINA_API_KEY
```

---

## Initialization

Before starting the API, generate the FAISS vector index by running:

```bash
python index.py
```

Start the application:

```bash
uvicorn main:app --reload
```

For production:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing:

```
GROQ_API_KEY=...
JINA_API_KEY=...
```

Generate the vector database:

```bash
python index.py
```

Run the API:

```bash
uvicorn main:app --reload
```
