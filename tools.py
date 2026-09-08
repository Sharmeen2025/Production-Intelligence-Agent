import os
import json
import urllib.request
from langchain_core.tools import tool
from duckduckgo_search import DDGS
from sqlalchemy import create_engine, text

@tool
def get_stock_price(ticker: str) -> str:
    """Fetch the current stock price for a given ticker symbol (e.g., NVDA, AAPL)."""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker.upper()}"
        # Spoofing a browser User-Agent so Yahoo doesn't block the cloud IP
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            price = data['chart']['result'][0]['meta']['regularMarketPrice']
            currency = data['chart']['result'][0]['meta']['currency']
            return f"The current live price of {ticker.upper()} is {price} {currency}."
    except Exception as e:
        return f"Failed to retrieve stock data for {ticker}: {e}"

@tool
def web_search(query: str) -> str:
    """Search the live web for general facts, current events, and recent news."""
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "Error: The search engine blocked the cloud IP (anti-bot protection). No results."
        
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
    """Evaluate simple mathematical expressions (e.g., '100 * 1.2')."""
    try:
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Only standard mathematical characters are permitted."
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def query_database(sql_query: str) -> str:
    """Execute a read-only SQL SELECT query against the PostgreSQL database."""
    try:
        engine = create_engine(os.getenv("DATABASE_URL"))
        with engine.connect() as conn:
            if not sql_query.strip().upper().startswith("SELECT"):
                return "Error: Security violation. Only SELECT queries permitted."
            result = conn.execute(text(sql_query))
            rows = result.fetchmany(50)
            if not rows:
                return "No records found matching query."
            return "\n".join([str(dict(row._mapping)) for row in rows])
    except Exception as e:
        return f"Database query failed: {e}"