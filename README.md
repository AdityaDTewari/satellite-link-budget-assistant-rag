# Satellite Link Budget Assistant (RAG + Angular Frontend)

This project is a **local Retrieval-Augmented Generation (RAG) system** for satellite link budget calculations, combining:

* **Backend**: FastAPI + Ollama (`phi3`) + FAISS vector database for document retrieval.
* **Frontend**: Angular standalone application with a chat interface.
* **RAG Pipeline**: Ingests SATCOM documents, chunks and embeds them, and retrieves relevant context to answer queries.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Backend Setup](#backend-setup)
4. [Document Ingestion & RAG](#document-ingestion--rag)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [Usage](#usage)
8. [Future Enhancements](#future-enhancements)

---

## Features

* Chat interface for satellite link budget questions.
* Local RAG system using Ollama (`phi3`) with vector search (FAISS).
* Supports PDF, TXT, Markdown, and DOCX SATCOM documents.
* Chunking and embedding of documents for retrieval.
* Displays document IDs in answers for traceability.
* Simple, clean Angular frontend with header and chat box.

---

## Project Structure

```
project-root/
├─ backend/
│  ├─ data/                # Raw SATCOM docs (PDFs, Markdown)
│  ├─ chunks/              # Preprocessed + chunked documents
│  ├─ embeddings/          # Embeddings for FAISS
│  ├─ vectordb/            # FAISS indices
│  ├─ ingest/
│  │   ├─ ingest.py        # Normalize PDF/TXT/MD/DOCX
│  │   └─ chunk_docs.py    # Split into chunks
│  ├─ models/
│  │   ├─ model_runner.py  # Calls Ollama CLI
│  │   ├─ retriever.py     # FAISS search + retrieval
│  │   └─ rag_runner.py    # RAG orchestration
│  ├─ api/
│  │   └─ app.py           # FastAPI endpoints
│  ├─ utils/
│  │   ├─ text_utils.py    # Text chunking
│  │   └─ file_utils.py    # File reading helpers
│  ├─ tests/
│  │   └─ smoke_test.py
│  └─ requirements.txt
├─ rag-ui/                  # Angular frontend
│  ├─ src/
│  │   ├─ app/
│  │   │   ├─ chat/         # Chat component
│  │   │   ├─ services/     # ApiService
│  │   │   ├─ models/       # Message model
│  │   │   ├─ app.routes.ts
│  │   │   └─ app.component.html/.ts/.css
│  │   └─ environments/
│  │       └─ environment.ts
│  └─ proxy.conf.json       # Proxy to backend during dev
└─ README.md
```

---

## Backend Setup

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
# .venv\Scripts\activate    # windows
pip install --upgrade pip
```

### 2. Install dependencies

```bash
pip install -r backend/requirements.txt
pip install transformers sentence-transformers
```

### 3. Ensure Ollama is installed

```bash
ollama serve
ollama pull phi3
```

---

## Document Ingestion & RAG

### 1. Ingest documents

```bash
python backend/ingest/ingest.py
```

* Converts PDFs/TXT/MD/DOCX to JSON chunks in `backend/chunks/docs`.

### 2. Chunk documents

```bash
python backend/ingest/chunk_docs.py
```

* Splits long documents into ~300 token chunks with overlap.

### 3. Build embeddings

```bash
python backend/embeddings/build_embeddings.py
```

* Generates vector embeddings with `SentenceTransformer`.

### 4. Build FAISS index

```bash
python backend/vectordb/build_faiss.py
```

* Normalizes embeddings and creates FAISS index for similarity search.

---

## Frontend Setup

### 1. Navigate to Angular project

```bash
cd rag-ui
```

### 2. Install dependencies

```bash
npm install
```

### 3. Proxy configuration

`proxy.conf.json` ensures Angular dev server can call FastAPI backend without CORS issues.

```json
{
  "/api": {
    "target": "http://127.0.0.1:8000",
    "secure": false,
    "changeOrigin": true,
    "pathRewrite": { "^/api": "" },
    "logLevel": "debug"
  }
}
```

### 4. Run Angular frontend

```bash
ng serve --proxy-config proxy.conf.json
```

* Open: `http://localhost:4200`
* The header "Satellite Assistant" appears at top.
* Chat messages appear below.

---

## Running the Full Application

1. Start **backend**:

```bash
uvicorn backend.api.app:app --reload --port 8000
```

2. Start **frontend**:

```bash
cd rag-ui
ng serve --proxy-config proxy.conf.json
```

3. Ask questions in chat, e.g.:

* "How to compute FSPL at 12 GHz for GEO satellite?"
* "Calculate antenna gain for a 1.2m dish at 12 GHz"

---

## Usage

* User types a question → Angular sends POST to `/api/query`.
* Backend retrieves top-K relevant document chunks → passes to Ollama LLM.
* Response shown in chat with context (document IDs optionally displayed).

---

## Future Enhancements

* Sidebar showing retrieved document snippets.
* File upload for new SATCOM PDFs.
* Structured numeric calculators exposed as agentic tools.
* Streaming LLM responses for better UX.
* Multiple model selection and adjustable RAG parameters.

---

## References

* [Ollama](https://ollama.com)
* [FAISS](https://faiss.ai)
* [Sentence Transformers](https://www.sbert.net/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Angular Standalone Components](https://angular.io/guide/standalone-components)
