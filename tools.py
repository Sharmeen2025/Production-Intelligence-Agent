import os
from langchain_core.tools import tool
from duckduckgo_search import DDGS
from sqlalchemy import create_engine, text

@tool
def web_search(query: str) -> str:
    """Search the live web for up-to-date information, news, or facts."""
    try:
        results = DDGS().text(query, max_results=3) 
        if not results:
            return "No results found."
        
        return "\n".join([f"- {res['title']}: {res['body']}" for res in results])
    except Exception as e:
        return f"Search failed: {e}"

@tool
def calculate_metrics(expression: str) -> str:
    """Evaluate simple mathematical expressions (e.g., '100 * 1.2' or '500 / 12')."""
    try:
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic mathematical characters are allowed."
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def query_database(sql_query: str) -> str:
    """Execute a SQL SELECT query against the PostgreSQL database. Use this to retrieve sales and product data."""
    try:
        # Create the engine dynamically when the tool is called
        engine = create_engine(os.getenv("DATABASE_URL"))
        with engine.connect() as conn:
            if not sql_query.strip().upper().startswith("SELECT"):
                return "Error: Security violation. Only SELECT queries are permitted."
            
            result = conn.execute(text(sql_query))
            rows = result.fetchmany(50) 
            
            if not rows:
                return "No results found."
            
            return "\n".join([str(dict(row._mapping)) for row in rows])
    except Exception as e:
        return f"Database query failed: {e}"