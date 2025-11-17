import logging
import os
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
    """Echo server - returns the input text."""
    return f"ECHO: {text}"


@mcp.tool()
def get_financial_agents() -> dict:
    """List available financial analysis agents."""
    return {
        "agents": [
            {"name": "CEO AI", "role": "Strategic Financial Analysis"},
            {"name": "CFO AI", "role": "Cash Flow & Budget Management"},
            {"name": "CMO AI", "role": "Market & Revenue Analysis"},
            {"name": "CRO AI", "role": "Risk Assessment"},
            {"name": "CIO/CISO AI", "role": "Security & IT Strategy"},
        ]
    }


if __name__ == "__main__":
    logging.info(f"Starting development server for '{APP_NAME}'...")
    mcp.run()
