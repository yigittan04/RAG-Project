# RAG Project

Retrieval-Augmented Generation application built with **FastAPI, React, FAISS, PostgreSQL, Jina AI Embeddings, and the Groq API**.

The application allows authenticated users to upload documents, process them into semantic vector embeddings, search their documents using FAISS, and generate context-aware answers with an LLM.

The system supports persistent conversations, document management, source retrieval, retrieval logging, user authentication, and a React-based web interface.

---

# How It Works

The application follows a RAG pipeline:

1. A user uploads a document through the web interface.

2. The document is loaded and cleaned.

3. The document is split into smaller chunks.

4. Each chunk is converted into a vector embedding using the **Jina AI Embeddings API**.

5. The embeddings are stored in a **FAISS vector database**.

6. Document, user, conversation, message, chunk, and retrieval information is stored in **PostgreSQL**.

7. When a user asks a question:

   * The question is converted into an embedding.
   * FAISS searches for the most semantically similar document chunks.
   * The retrieved chunks are used as context.
   * Relevant conversation history is included in the prompt.
   * The context is sent to the Groq-hosted LLM.
   * The LLM generates an answer using the retrieved context.

8. The question and generated answer are stored as messages inside the user's conversation.

9. Retrieval information such as similarity, rank, and retrieval latency is stored for the retrieved chunks.

The API returns the generated answer together with the source chunks used during retrieval.

---

# Features

## RAG

* Retrieval-Augmented Generation
* Semantic document search
* FAISS vector database
* Jina AI embeddings
* Context-aware answer generation
* Source document retrieval
* Document-specific questioning
* Document summarization
* Document overview questions
* Conversation-aware questions

## Authentication

* User registration
* User login
* JWT-based authentication
* Password hashing
* Authenticated API access
* User account information
* Protected user resources

## Documents

* PDF document upload
* DOCX document upload
* TXT document upload
* Automatic document processing
* Automatic text cleaning
* Automatic chunking
* Automatic embedding generation
* Document ownership
* Document listing
* Document details
* Document deletion
* SHA-256 duplicate file detection
* FAISS vector deletion
* Upload transaction rollback protection

## Conversations

* Persistent conversations
* Conversation history
* Persistent user and assistant messages
* Conversation-specific questions
* Conversation ownership
* Conversation retrieval
* Conversation archiving

## Retrieval Logging

The application records information about the retrieval process, including:

* Retrieved chunk
* Similarity score
* Retrieval rank
* Retrieval latency
* Associated message

## Frontend

* React
* Vite
* Login interface
* Registration interface
* Chat interface
* Conversation navigation
* Document management
* Document selection
* Authenticated user interface
* Persistent conversation interface

## API

* REST API built with FastAPI
* Automatic Swagger/OpenAPI documentation
* JWT authentication
* CORS support
* Structured API endpoints
* Protected resources
* PostgreSQL persistence

## Deployment

* Render frontend deployment
* Render backend deployment
* Neon PostgreSQL database
* FAISS vector storage
* Environment-based configuration

---

# Technologies

## Backend

* FastAPI
* Pydantic
* SQLAlchemy
* Uvicorn

## Database

* PostgreSQL
* SQLAlchemy ORM
* Neon PostgreSQL

The database stores users, conversations, messages, documents, document chunks, and retrieval logs.

## Retrieval

* FAISS
* NumPy

## Embeddings

* Jina AI Embeddings API

## LLM

* Groq API
* GPT-OSS-120B

The current generator uses the `openai/gpt-oss-120b` model through Groq.

## Document Processing

* PyMuPDF
* python-docx
* Text cleaning utilities
* Text chunking utilities

## Frontend

* React
* Vite
* JavaScript
* CSS

## Deployment

* Render
* Neon PostgreSQL

---

# Project Structure

```text
rag_project/
│
├── data/
│
├── database/
│   ├── crud.py
│   ├── database.py
│   └── models.py
│
├── embeddings/
│   └── embedding.py
│
├── generation/
│   └── prompt_builder.py
│
├── generator/
│   └── generator.py
│
├── preprocessing/
│   ├── loader.py
│   ├── cleaner.py
│   └── chunker.py
│
├── prompts/
│
├── retrieval/
│   ├── store.py
│   └── vector_store.py
│
├── router/
│   ├── auth.py
│   ├── conversations.py
│   └── documents.py
│
├── uploads/
│
├── utils/
│
├── vector_store/
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── config.py
├── index.py
├── main.py
├── security.py
├── requirements.txt
├── run.sh
└── .env.example
```

The repository also contains runtime architecture documentation describing the application's structure and data flow.

---

# API

## Authentication

### POST `/auth/register`

Creates a new user account.

Example request:

```json
{
  "username": "user",
  "email": "user@example.com",
  "password": "password"
}
```

### POST `/auth/login`

Authenticates a user and returns a JWT access token.

Example request:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Example response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### GET `/auth/me`

Returns information about the currently authenticated user.

---

# Documents API

## POST `/documents/upload`

Uploads and processes a document.

Supported document types:

* PDF
* DOCX
* TXT

The upload pipeline:

1. Reads the uploaded file.
2. Calculates a SHA-256 hash.
3. Checks for duplicate documents.
4. Stores the uploaded file.
5. Creates the document record.
6. Loads and cleans the document.
7. Splits the document into chunks.
8. Generates embeddings.
9. Stores the chunks in PostgreSQL.
10. Adds the vectors to FAISS.

Example response:

```json
{
  "document_id": "document-uuid",
  "filename": "example.pdf",
  "status": "processed",
  "chunk_count": 12
}
```

Duplicate files are rejected to prevent the same document from being uploaded multiple times.

## GET `/documents`

Returns the documents belonging to the authenticated user.

## GET `/documents/{document_id}`

Returns information about a specific document.

## DELETE `/documents/{document_id}`

Deletes a document and its associated vector data.

Document ownership is checked before accessing or deleting documents.

---

# Conversations API

## POST `/conversations`

Creates a new conversation.

## GET `/conversations`

Returns the authenticated user's conversations.

## GET `/conversations/{conversation_id}`

Returns a specific conversation.

## GET `/conversations/{conversation_id}/messages`

Returns the messages belonging to a conversation.

## PATCH `/conversations/{conversation_id}/archive`

Archives a conversation.

Conversation access is restricted to the user who owns the conversation.

---

# RAG API

## POST `/ask`

Accepts a natural language question.

The request can optionally specify a conversation and a document.

Example request:

```json
{
  "question": "What is Python?",
  "conversation_id": null,
  "document_id": null
}
```

Example response:

```json
{
  "conversation_id": "conversation-uuid",
  "user_message_id": "message-uuid",
  "assistant_message_id": "message-uuid",
  "question": "What is Python?",
  "answer": "Python is a programming language.",
  "sources": [
    "Python is a programming language."
  ]
}
```

The `/ask` endpoint requires authentication and verifies ownership of the selected conversation and document.

For normal questions, FAISS retrieves the top three relevant chunks.

For broad questions about a selected document, such as:

* Summarize this document.
* Give me an overview.
* What are the main topics?
* What does this document cover?

the system can use the stored chunks of the selected document as context instead of limiting retrieval to the top three semantic matches.

---

# Database

The application uses PostgreSQL to persist application data.

The database contains the following main entities:

* Users
* Conversations
* Messages
* Documents
* Chunks
* Retrieval Logs

Relationships between these entities allow the application to maintain user-specific documents, conversations, messages, and retrieval information.

---

# Vector Database

FAISS is used for semantic vector search.

Each processed document is divided into chunks.

The chunks are converted into embeddings and stored in the FAISS vector store together with metadata identifying the corresponding document and chunk.

When a user asks a question:

1. The question is converted into an embedding.
2. FAISS compares the question embedding against stored vectors.
3. The most relevant chunks are retrieved.
4. The retrieved chunks are passed to the prompt builder.
5. The resulting prompt is sent to the LLM.

The vector store also supports document-specific retrieval and document vector deletion.

---

# Security

The application uses JWT authentication to protect authenticated functionality.

Passwords are hashed before being stored.

Users can only access their own:

* Documents
* Conversations
* Messages
* Document-specific retrieval results

The `/ask`, document, and conversation operations validate the authenticated user's ownership before accessing user-specific resources.

API keys and database credentials are provided through environment variables and are not stored directly in the source code.

---

# Deployment

The project is deployed using **Render** with separate frontend and backend services.

## Live Frontend

The React frontend is deployed as a Render web service:

**https://rag-project-frontend-mvye.onrender.com**

The frontend provides the user interface for:

* Registration
* Login
* Chat
* Conversations
* Document management
* Document-specific questions

## Backend API

The FastAPI backend is deployed separately as a Render web service:

**https://rag-project-icjj.onrender.com**

Swagger / OpenAPI documentation:

**https://rag-project-icjj.onrender.com/docs**

The backend provides the REST API used by the frontend.

---

# Render Services

The deployed application consists of the following services:

### Frontend

* Platform: Render
* Application: React + Vite
* Type: Render Web Service / frontend service
* Purpose: User interface

### Backend

* Platform: Render
* Application: FastAPI
* Type: Render Web Service
* Purpose: REST API, authentication, RAG processing, document processing, and generation

### Database

* Platform: Neon
* Type: PostgreSQL
* Purpose: Persistent application data

### Vector Database

* Technology: FAISS
* Purpose: Semantic vector search and document retrieval

The frontend and backend are deployed separately so that the React application communicates with the FastAPI API.

---

# Environment Variables

The application uses environment variables for configuration and secrets.

Required backend variables include:

```text
DATABASE_URL
GROQ_API_KEY
HF_HOME
JINA_API_KEY
INDEX_USER_ID
JWT_SECRET_KEY
```

A local `.env` file can be used during development.

Example:

```text
DATABASE_URL=...
GROQ_API_KEY=...
HF_HOME=...
JINA_API_KEY=...
INDEX_USER_ID=...
JWT_SECRET_KEY=...
```

---

# Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/yigittan04/RAG-Project.git
cd RAG-Project
```

## 2. Install backend dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

Create a `.env` file:

```text
DATABASE_URL=...
GROQ_API_KEY=...
HF_HOME=...
JINA_API_KEY=...
INDEX_USER_ID=...
JWT_SECRET_KEY=...
```

## 4. Start the backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# Running the Frontend

The frontend is built with React and Vite.

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

The frontend communicates with the FastAPI backend through the API service layer.

---

# Frontend Deployment

For the Render frontend service, the frontend can be built using:

```bash
npm install
npm run build
```

The production build is generated in:

```text
frontend/dist/
```

The Render frontend service serves the generated React application.

The deployed frontend is available at:

```text
https://rag-project-frontend-mvye.onrender.com
```

---

# Application Flow

```text
                    ┌──────────────────────┐
                    │   Render Frontend    │
                    │     React + Vite     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Render Backend     │
                    │ FastAPI REST API     │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       ┌──────────┐      ┌────────────┐     ┌──────────┐
       │   JWT    │      │ PostgreSQL │     │  FAISS   │
       │   Auth   │      │   Neon DB  │     │  Search  │
       └──────────┘      └────────────┘     └────┬─────┘
                                                  │
                                                  ▼
                                           Retrieved Chunks
                                                  │
                                                  ▼
                                          ┌──────────────┐
                                          │  Groq API    │
                                          │ GPT-OSS-120B │
                                          └──────┬───────┘
                                                 │
                                                 ▼
                                              Answer
```

---

# RAG Pipeline

```text
Document
   │
   ▼
Document Loader
   │
   ▼
Text Cleaning
   │
   ▼
Text Chunking
   │
   ▼
Jina AI Embeddings
   │
   ▼
FAISS Vector Store
   │
   │
   │ User Question
   ▼
Question Embedding
   │
   ▼
Semantic Search
   │
   ▼
Relevant Chunks
   │
   ▼
Prompt Builder
   │
   ▼
Groq GPT-OSS-120B
   │
   ▼
Generated Answer
   │
   ├──► Conversation History
   ├──► Source Chunks
   └──► Retrieval Logs
```

---

# Project Status

The project currently provides a full RAG workflow with:

* User authentication
* JWT authorization
* Persistent PostgreSQL storage
* Neon PostgreSQL deployment
* Document upload and processing
* PDF, DOCX, and TXT support
* Automatic document chunking
* Jina AI embeddings
* FAISS semantic retrieval
* Document-specific retrieval
* Document summarization and overview questions
* Groq LLM generation
* GPT-OSS-120B
* Persistent conversations
* Conversation history
* Document management
* SHA-256 duplicate detection
* Retrieval logging
* Source retrieval
* React/Vite frontend
* Render frontend deployment
* Render backend deployment
* Swagger/OpenAPI documentation

The system is designed as a modular RAG application where document processing, embeddings, retrieval, generation, database operations, API routing, authentication, and frontend functionality are separated into dedicated components.
