A production-ready **Retrieval-Augmented Generation (RAG)** system with multi-language support, hybrid database architecture, and a web-based interface.

---

## 📋 Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [How Files Work Together](#how-files-work-together)
- [Startup Sequence](#startup-sequence)
- [Request Flow](#request-flow)
- [Component Details](#component-details)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)

---

## 🎯 Overview

This RAG system provides intelligent document querying capabilities with:

- **Hybrid Database**: SQLite (metadata) + Milvus (vectors)
- **Multi-language Support**: English and Korean
- **OCR Processing**: Handles image-based PDFs
- **Web Interface**: Streamlit GUI for easy access
- **Production Ready**: Docker deployment and robust error handling

### Technology Stack
- **Backend**: FastAPI, Python 3.8+
- **Vector DB**: Milvus 2.3.3
- **Metadata DB**: SQLite 3
- **LLM**: Ollama (`llama3:8b`)
- **Embeddings**: Ollama (`nomic-embed-text`)
- **Frontend**: Streamlit
- **OCR**: Tesseract + Poppler

---

## 🏗️ System Architecture
```
┌─────────────────────────────────────────────────────────┐
│ Presentation Layer (API)                                │
│ main.py → routes.py → query.py / upload.py              │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│ Business Logic Layer                                    │
│ rag_engine.py (orchestrates everything)                 │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
 ┌──────────────┐                 ┌──────────────┐
 │ database.py  │                 │     llm.py   │
 │ SQLite +     │                 │    Ollama    │
 │ Milvus       │                 │              │
 └──────────────┘                 └──────────────┘
```

---

## 🔗 How Files Work Together

### Core File Structure
```
project/
├── main.py # 🚀 Entry point - FastAPI app
├── config.py # ⚙️ Configuration center
├── routes.py # 🛣️ Route aggregation
├── query.py # ❓ Query handler
├── upload.py # 📤 Upload handler
├── rag_engine.py # 🧠 RAG core logic
├── database.py # 💾 Hybrid DB (SQLite + Milvus)
├── llm.py # 🤖 LLM service
├── models.py # 📋 Data models
├── validation.py # ✅ Input validation
├── security.py # 🔒 Security checks
├── logger.py # 📝 Logging setup
└── gui_layer.py # 🖥️ Streamlit web interface
```

### File Dependencies
```
main.py
├── config.py
├── routes.py
│ ├── query.py
│ │ ├── rag_engine.py
│ │ │ └── database.py
│ │ ├── llm.py
│ │ ├── validation.py
│ │ └── security.py
│ └── upload.py
│ └── rag_engine.py
├── logger.py
└── models.py
```

---

## 🚀 Startup Sequence

When you run `python main.py`, the following occurs:

1. **main.py loads**
   - Reads configuration
   - Initializes logging
   - Registers API routes

2. **routes.py loads**
   - Registers query and upload endpoints

3. **Query & Upload modules load**
   - Initialize validation, security, RAG engine, and LLM services

4. **RAG Engine initializes**
   - Loads embedding model
   - Prepares query pipeline

5. **Database connects**
   - SQLite database initialized
   - Milvus vector collections prepared

6. **Lifespan function runs**
   - Checks LLM availability
   - Loads existing documents

7. **Server starts**
   - API available at `http://localhost:8000`

---

## 📊 Request Flow

### Query Request Flow
```
User → POST /query/query
→ main.py
→ routes.py
→ query.py
├── validation.py
├── security.py
└── rag_engine.py
├── database.py (Milvus + SQLite)
└── llm.py (Ollama)
→ Response returned to user
```

### Upload Request Flow
```
User → POST /upload/document
→ upload.py
├── File validation
├── Security checks
└── rag_engine.py
├── OCR/Text extraction
├── Chunking
├── Embedding
└── Store in SQLite + Milvus
```

---

## 📦 Component Details

### 1. main.py – Application Entry Point
- Creates FastAPI application
- Registers routes and middleware
- Starts the API server

### 2. config.py – Configuration Center
- Centralized system settings
- Database, LLM, RAG, and API configuration
- Supports environment variable overrides

### 3. routes.py – Route Aggregator
- Organizes query and upload endpoints
- Applies route prefixes

### 4. query.py – Query Handler
- Validates input
- Applies security checks
- Executes RAG query pipeline

### 5. upload.py – Document Handler
- Validates and sanitizes files
- Saves documents
- Indexes content into vector DB

### 6. rag_engine.py – RAG Core
- Language detection (EN/KO)
- Embedding generation
- Vector search
- Context building and answer generation

### 7. database.py – Hybrid Database
- SQLite for metadata
- Milvus for vector embeddings
- Joins vector results with document metadata

### 8. llm.py – LLM Service
- Communicates with Ollama
- Generates final responses
- Health checks for availability

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (for Milvus)
- Ollama installed and running
- Tesseract OCR (for scanned PDFs)

### Installation

```bash
cd Synapse_X_RAG
python -m venv .venv
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
Start Milvus
docker-compose up -d
Start FastAPI Server
python main.py
Start Streamlit GUI (Optional)
streamlit run gui_layer.py

🔌 API Endpoints
Query
POST /query/query

GET /query/health

Upload
POST /upload/document

GET /upload/status

POST /upload/rebuild

System Health
GET /health

⚙️ Configuration
Environment Variables
# Database
export MILVUS_HOST=localhost
export MILVUS_PORT=19530

# LLM
export OLLAMA_MODEL=llama3:8b
export OLLAMA_EMBED_MODEL=nomic-embed-text

# API
export API_HOST=0.0.0.0
export API_PORT=8000

# RAG
export CHUNK_SIZE=2048
export SIMILARITY_TOP_K=8
Default Configuration
See config.py for full configuration options.
```

🎯 Key Features
✅ Hybrid Database (SQLite + Milvus)

✅ Multi-language (English / Korean)

✅ OCR support for scanned PDFs

✅ Web-based UI

✅ Production-ready architecture

✅ Fast semantic search

✅ Scalable to large document sets


📄 License
This project is part of a Capstone Design Project.


👤 Author
Shalkar
Enterprise AI Assistant – RAG System
