import logging
import os
import random
import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
load_dotenv()
# --- Configuration ---
APP_NAME = os.getenv("APP_NAME", "Default-MCP-Server")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
# --- Logging Setup ---
logging.basicConfig(level=LOG_LEVEL, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
mcp = FastMCP(APP_NAME)
@mcp.tool()
def echo(text: str) -> str:
    """
    Returns the same text it receives.
    Args:
        text: The text to repeat.
    logging.info(f"Echoing: {text}")
    return text
def get_financial_agents() -> dict:
    Returns a list of available financial agent personas.
    return {
        "agents": [
            {"name": "Risk Analyst", "id": "agent-01"},
            {"name": "Portfolio Manager", "id": "agent-02"},
            {"name": "Compliance Officer", "id": "agent-03"},
        ]
    }
def get_stock_price(ticker: str) -> dict:
    Returns a fictional stock price for a given ticker symbol.
        ticker: The stock ticker symbol (e.g., 'AAPL').
    Returns:
        A dictionary containing the ticker and its fictional price.
    # Generate a fictional price, for example between 50 and 1000
    price = round(random.uniform(50.0, 1000.0), 2)
    logging.info(f"Generated fictional price for {ticker}: ${price}")
        "ticker": ticker.upper(),
        "price": price,
        "currency": "USD"
if __name__ == "__main__":
    logging.info(f"Starting development server for '{APP_NAME}'...")
    mcp.run()
