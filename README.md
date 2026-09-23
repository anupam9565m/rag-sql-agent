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
