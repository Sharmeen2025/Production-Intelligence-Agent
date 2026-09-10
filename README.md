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
    
The core orchestration engine is built on **LangGraph**, routing queries through a resilient execution loop. The agent evaluates the request, validates tool schemas, executes the tool, and self-corrects if external systems (e.g., databases or APIs) return execution errors.

## Core Capabilities
*   **Stateful Memory:** Manages complex, multi-step conversation context without context degradation.
*   **SQL Database Integration:** Secure, read-only PostgreSQL querying with strict row-limit guardrails.
*   **Live Web Retrieval:** Grounded knowledge extraction using web search pipelines.
*   **Deterministic Computation:** Isolated mathematical evaluation sandbox.

## Technology Stack
*   **Orchestration:** LangGraph, LangChain Core
*   **Inference:** Groq LPU API 
*   **Database:** Neon Serverless PostgreSQL, SQLAlchemy
*   **Interface:** Streamlit

## Setup and Local Execution
1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Configure your `.env` file with your `GROQ_API_KEY` and Neon `DATABASE_URL`.
4. Initialize the database schema: `python seed.py`
5. Launch the application: `python -m streamlit run app.py`

## Acknowledgements
* The open-source communities behind LangChain, LangGraph, and Streamlit.
* Groq for the high-speed model inference.
* Neon for the serverless PostgreSQL architecture.

## Author
**Sharmeen Bukhtawar**  
MSc Artificial Intelligence & Data Science  
BSc (Hons) Biomedical Science  
GitHub: [https://github.com/Sharmeen2025](https://github.com/Sharmeen2025)  
LinkedIn: [https://www.linkedin.com/in/sharmeen-bukhtawar-2b0568265/](https://www.linkedin.com/in/sharmeen-bukhtawar-2b0568265/)

## License
This project is licensed under the MIT License - see the LICENSE file for details.