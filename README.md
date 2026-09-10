# Production Intelligence Agent

An autonomous, state-machine-driven AI agent built to execute deterministic business workflows. Unlike standard conversational text models or document-constrained RAG pipelines, this system utilizes a cyclical orchestration architecture to autonomously select and execute external tools, ensuring grounded data retrieval and mathematical accuracy.

## System Architecture

```mermaid
graph TD
    A[User Query] --> B(LangGraph State Machine)
    B -->|Action Required| C{Tool Router}
    C -->|Yahoo Finance API| D[Stock Retriever]
    C -->|DuckDuckGo| E[Web Search]
    C -->|SQLAlchemy| F[PostgreSQL DB]
    D & E & F -->|Observations| B
    B -->|Final Synthesis| G[Streamlit Interface]
