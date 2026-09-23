# rag-sql-agent
Hybrid RAG agent using LangChain, pgvector, and FastAPI to execute natural language queries against SQL databases and vector stores
# 🤖 Enterprise RAG Agent with SQL & Vector Database Integration

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.14-1C3C3C.svg?logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1.svg?logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)

An enterprise-grade hybrid retrieval engine that unifies structured relational database execution (`PostgreSQL`) and unstructured context retrieval (`pgvector`) into a single ReAct agent interface. Built with **LangChain**, **FastAPI**, and **Docker**, the system dynamically routes queries between database schemas and vector indexes to answer multi-modal data questions with high accuracy.

---

## 💡 System Architecture

```text
                               +-----------------------------------+
                               |     User / Client Application     |
                               +-----------------------------------+
                                                 |
                                       HTTP POST /query
                                                 v
                               +-----------------------------------+
                               |       FastAPI Service Engine      |
                               +-----------------------------------+
                                                 |
                                       LangChain ReAct Agent
                                       (GPT-4o / Embeddings)
                                                 |
                      +--------------------------+--------------------------+
                      |                                                     |
                      v                                                     v
         +--------------------------+                         +--------------------------+
         |  SQL Database Toolkit    |                         |  pgvector Retrieval Tool |
         +--------------------------+                         +--------------------------+
                      |                                                     |
            Text-to-SQL Execution                                Embedding Similarity Search
                      |                                                     |
                      +--------------------------+--------------------------+
                                                 |
                                                 v
                               +-----------------------------------+
                               |  PostgreSQL Database (pgvector)   |
                               |  - Relational: customers, orders  |
                               |  - Vector: product_knowledge      |
                               +-----------------------------------+










rag-sql-agent/
├── app/
│   ├── __init__.py          # Module initialization
│   ├── config.py            # Environment validation & Pydantic settings
│   ├── database.py          # SQLAlchemy engine & SQLDatabase initialization
│   ├── agent.py             # ReAct Agent assembly with hybrid toolsets
│   └── main.py              # FastAPI application server & REST endpoints
├── scripts/
│   └── seed_db.py           # DDL schema setup, relational seeding & vector indexing
├── .env                     # Local environment variables (Git ignored)
├── .gitignore               # Version control rules
├── Dockerfile               # Python 3.11 container manifest
├── docker-compose.yml       # Multi-container orchestration (FastAPI + pgvector)
└── requirements.txt         # Fixed production dependencies


Technologies & Frameworks:
- Languages & Core: Python 3.11, SQL (PostgreSQL), REST APIs
- Frameworks & Libraries: FastAPI, LangChain, SQLAlchemy, Pydantic, PyPDF/Unstructured
- AI & Vector Search: OpenAI GPT-4o, OpenAI Text-Embeddings, pgvector, Vector Embeddings, ReAct Agent Architecture
- Database & Infrastructure: PostgreSQL 16, pgvector Extension, Docker, Docker Compose, Uvicorn


🚀 Quickstart Guide
Prerequisites
Docker Desktop installed and running.

An OpenAI API Key.
Step-by-step Instructions
1. Clone the Repository
Bash
git clone [https://github.com/anupam9565m/rag-sql-agent.git](https://github.com/anupam9565m/rag-sql-agent.git)
cd rag-sql-agent
2. Configure Environment
Create a .env file in the root directory:

Bash
# Linux / macOS
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
Edit .env and add your OpenAI API key:

Ini, TOML
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=rag_sql_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
3. Spin Up Infrastructure via Docker Compose
Build images and start containerized services:

Bash
docker-compose up --build -d
Verify that both postgres_vector_db and rag_sql_agent_api containers are healthy:

Bash
docker-compose ps
4. Seed Relational Data and Vector Indexes
Run the initialization script inside the API container to create schemas, relational data, and vector embeddings:

Bash
docker exec -it rag_sql_agent_api python scripts/seed_db.py
Git.





