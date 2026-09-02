import os
from langchain_core.tools import tool
from duckduckgo_search import DDGS
from sqlalchemy import create_engine, text

@tool
def web_search(query: str) -> str:
    """Search the live web for real-time facts, current events, live stock prices, market data, and recent news."""
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No relevant live web results found."
        
        formatted_results = []
        for res in results:
            title = res.get("title", "No Title")
            body = res.get("body", "No Body")
            formatted_results.append(f"Title: {title}\nSnippet: {body}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Live search failed: {e}"

@tool
def calculate_metrics(expression: str) -> str:
    """Evaluate simple mathematical expressions (e.g., '100 * 1.2' or '500 / 12')."""
    try:
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only standard mathematical characters are permitted."
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def query_database(sql_query: str) -> str:
    """Execute a read-only SQL SELECT query against the PostgreSQL database to retrieve sales and product data."""
    try:
        engine = create_engine(os.getenv("DATABASE_URL"))
        with engine.connect() as conn:
            if not sql_query.strip().upper().startswith("SELECT"):
                return "Error: Security violation. Only SELECT queries are permitted."
            
            result = conn.execute(text(sql_query))
            rows = result.fetchmany(50)
            
            if not rows:
                return "No records found matching query."
            
            return "\n".join([str(dict(row._mapping)) for row in rows])
    except Exception as e:
        return f"Database query failed: {e}"