# Website Intelligence Engine

## Overview

Website Intelligence Engine is a Retrieval-Augmented Generation (RAG) platform that can crawl websites, generate embeddings, store knowledge in Pinecone, and answer user questions using Groq Llama models.

The system supports website-specific question answering with source citations and web-search fallback using Tavily when confidence is low.

---

## Features

* Recursive website crawling
* Content cleaning
* Text chunking with overlap
* Sentence Transformer embeddings
* Pinecone vector storage
* Semantic retrieval
* Groq Llama-powered answers
* Source citations
* Tavily fallback search
* FastAPI backend

---

## Architecture

Website URL
↓
Crawler
↓
Cleaner
↓
Chunker
↓
Embeddings
↓
Pinecone

User Question
↓
Retriever
↓
Confidence Check
├── Website Context
└── Tavily Fallback
↓
Groq Llama
↓
Answer + Sources

---

## Tech Stack

Backend:

* FastAPI

Embeddings:

* Sentence Transformers (all-MiniLM-L6-v2)

Vector Database:

* Pinecone

LLM:

* Groq (Llama 3.3 70B)

Fallback Search:

* Tavily

Frontend:

* Flutter Web

---

## Installation

```bash
git clone <repo-url>
cd website-intelligence-engine-rag

pip install -r requirements.txt
```

Create a `.env` file:

```env
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
GROQ_API_KEY=
TAVILY_API_KEY=
```

Run:

```bash
uvicorn backend.app.main:app --reload
```

---

## API Endpoints

### POST /ingest

Request:

```json
{
  "url": "https://claysys.com"
}
```

Response:

```json
{
  "pages_crawled": 36,
  "chunks_stored": 452
}
```

---

### POST /ask

Request:

```json
{
  "question": "What services does ClaySys provide?"
}
```

Response:

```json
{
  "answer": "...",
  "sources": [
    "https://claysys.com"
  ],
  "source_type": "website"
}
```

---

## Future Improvements

* Hybrid retrieval
* BM25 search
* Knowledge graph visualization
* Multi-website indexing
* Analytics dashboard
