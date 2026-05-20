![CI](https://github.com/rahuln2002/EAIKA/actions/workflows/ci.yml/badge.svg)
# Enterprise AI Knowledge Assistant (EAIKA)

Production-grade Enterprise RAG Platform with Hybrid Retrieval, Cross-Encoder Reranking, Streaming AI Chat, Summarization, Observability, and Multi-Tenant Architecture.

---

# 🚀 Features

## 🤖 Enterprise RAG Pipeline

* Hybrid Retrieval (BM25 + Dense Retrieval)
* Cross-Encoder Reranking
* Context-Aware Generation
* Source Attribution & Citations
* Retrieval Evaluation Framework

## 💬 Real-Time AI Chat

* WebSocket Streaming
* Token-by-Token Response Streaming
* ChatGPT-like User Experience
* Multi-Session Conversations

## 📄 Document Intelligence

* PDF Upload & Parsing
* DOCX Support
* Semantic Chunking
* Metadata Extraction
* Recursive Chunking Pipeline

## 🧠 Summarization System

* Map-Reduce Summarization
* Executive Summaries
* Long Document Processing
* Hierarchical Summarization

## 🔍 Enterprise Retrieval

* Hybrid Search Architecture
* BM25 Lexical Retrieval
* Dense Vector Retrieval
* Cross-Encoder Reranking
* Qdrant Vector Database

## 📊 AI Evaluation & Analytics

* Faithfulness Evaluation
* Hallucination Detection
* Retrieval Relevancy Scoring
* Retrieval Metrics
* RAG Evaluation Framework

## 🔐 Security & Multi-Tenancy

* JWT Authentication
* User-Isolated Retrieval
* Tenant-Aware Search
* Protected APIs
* Secure WebSocket Authentication

## ⚡ Scalability & Infrastructure

* Dockerized Architecture
* Kubernetes Deployment
* Celery Background Workers
* Redis Caching
* PostgreSQL Storage

## 📈 Observability & Monitoring

* OpenTelemetry Tracing
* Prometheus Metrics
* Structured Logging
* Request Latency Tracking
* Distributed Tracing

---

# 🏗️ System Architecture

```text
Frontend (Next.js)
        ↓
Nginx Reverse Proxy
        ↓
FastAPI Backend
   ├── Authentication
   ├── RAG Pipeline
   ├── Retrieval Layer
   ├── Summarization Engine
   ├── Analytics & Evaluation
   ├── WebSocket Streaming
   └── Background Workers
        ↓
Qdrant Vector Database
PostgreSQL
Redis
Celery
OpenTelemetry
```

---

# 🛠️ Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* Alembic
* Celery
* Redis
* PostgreSQL
* Qdrant
* OpenTelemetry
* Prometheus

## AI / NLP

* Groq
* Sentence Transformers
* Cross-Encoder Reranking
* BM25 Retrieval

## Frontend

* Next.js 15
* React 19
* TypeScript
* TailwindCSS
* Zustand
* React Query
* WebSockets

## Infrastructure

* Docker
* Docker Compose
* Kubernetes
* Nginx

---

# 📂 Project Structure

```text
backend/
frontend/
infrastructure/
docs/
data/
scripts/
```

---

# ⚙️ Environment Variables

Create:

```bash
.env.local
```

Example:

```env
# =====================================================
# DATABASE
# =====================================================

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/enterprise_ai_ka

# =====================================================
# REDIS
# =====================================================

REDIS_URL=redis://redis:6379/0

# =====================================================
# QDRANT
# =====================================================

QDRANT_HOST=qdrant
QDRANT_PORT=6333

# =====================================================
# GROQ
# =====================================================

GROQ_API_KEY=

# =====================================================
# JWT
# =====================================================

JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# 🐳 Docker Deployment

## Start Full Platform

From:

```bash
infrastructure/docker/
```

Run:

```bash
docker compose up --build
```

---

# 🗄️ Database Migrations

Enter backend container:

```bash
docker exec -it eaika-backend bash
```

Generate migration:

```bash
alembic revision --autogenerate -m "initial schema"
```

Apply migration:

```bash
alembic upgrade head
```

---

# 🌐 Access Services

| Service          | URL                             |
| ---------------- | ------------------------------- |
| Frontend         | http://localhost:3000           |
| Backend API      | http://localhost:8000           |
| Swagger Docs     | http://localhost:8000/docs      |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

# ☸️ Kubernetes Deployment

Kubernetes manifests are available inside:

```text
infrastructure/kubernetes/
```

Deploy:

```bash
kubectl apply -f infrastructure/kubernetes/
```

---

# 📡 API Endpoints

## Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

## Chat

```http
POST /api/v1/chat
WS   /ws/chat
```

## Upload

```http
POST /api/v1/upload
```

## Search

```http
GET /api/v1/search
```

## Summarization

```http
POST /api/v1/summarization
```

## Analytics

```http
GET /api/v1/analytics
```

---

# 🧠 RAG Pipeline

```text
User Query
    ↓
Hybrid Retrieval
(BM25 + Dense)
    ↓
Cross-Encoder Reranking
    ↓
Context Selection
    ↓
LLM Generation
    ↓
Source Attribution
    ↓
Evaluation Layer
```

---

# 🔍 Hybrid Retrieval Architecture

The retrieval system combines:

* BM25 Lexical Retrieval
* Dense Semantic Retrieval
* Cross-Encoder Reranking

This improves:

* semantic understanding
* exact keyword matching
* acronym retrieval
* retrieval precision

---

# 📊 Evaluation Framework

The platform includes enterprise-grade RAG evaluation:

## Metrics

* Faithfulness Score
* Hallucination Score
* Retrieval Relevancy
* Retrieval Metrics

## Purpose

* Measure grounding quality
* Detect hallucinations
* Evaluate retrieval quality
* Improve observability

---

# 📄 Summarization Pipeline

```text
Document
   ↓
Chunking
   ↓
Map Summaries
   ↓
Reduce Summary
   ↓
Executive Summary
```

Supports:

* long-document summarization
* hierarchical summarization
* enterprise summarization workflows

---

# 🔐 Multi-Tenant Architecture

The platform supports:

* user-isolated retrieval
* ownership-aware search
* secure document access
* protected vector retrieval

Each user retrieves ONLY their own uploaded documents.

---

# 📈 Observability

Integrated enterprise observability stack:

* OpenTelemetry Tracing
* Prometheus Metrics
* Structured Logging
* Request Latency Tracking

---

# 📊 Performance Metrics (Soon...)

<!-- | Metric                              | Value   |
| ----------------------------------- | ------- |
| Retrieval Latency                   | ~120ms  |
| Streaming Response Latency          | ~1.4s   |
| Hybrid Retrieval Recall Improvement | +18%    |
| Reranking Precision Improvement     | +22%    |
| Concurrent WebSocket Support        | Enabled | -->

---

# 📸 Screenshots (Soon...)

```text
docs/screenshots/
```

---

# 🧪 Future Improvements

* Reciprocal Rank Fusion (RRF)
* LangGraph Agent Workflows
* Multi-Agent Systems
* Tool Calling
* GPU Inference
* Llama.cpp Integration
* Local LLM Support
* Role-Based Access Control (RBAC)
* PDF Page-Level Citations
* Grafana Dashboards
* CI/CD Pipelines
* Helm Charts
* AWS/GCP Deployment

---

# 🎯 Resume-Level Highlights

* Built a production-grade enterprise RAG platform with hybrid retrieval, reranking, and streaming AI chat.
* Implemented multi-tenant user-isolated retrieval with secure WebSocket authentication.
* Designed scalable AI infrastructure using FastAPI, Next.js, Qdrant, PostgreSQL, Redis, Docker, and Kubernetes.
* Developed enterprise observability using OpenTelemetry, Prometheus, and structured logging.
* Created map-reduce summarization pipelines for long-document intelligence systems.

---

# 📚 Learning Outcomes

This project demonstrates:

* LLM Engineering
* RAG Systems
* GenAI Infrastructure
* AI System Design
* Full-Stack AI Development
* MLOps / LLMOps
* Distributed Systems
* Enterprise Backend Engineering
* Cloud-Native Deployment

---

# 👨‍💻 Author

Rahul Nihalani

Master's Student in AIML
AI Engineer | NLP | GenAI | RAG | LLM Systems

---

# ⭐ If You Like This Project

Star the repository and contribute!

---
