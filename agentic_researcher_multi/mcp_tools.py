# mcp_tools.py
import os
from dotenv import load_dotenv
import requests
from langchain.tools import tool

load_dotenv()
MCP_SEARCH_ENDPOINT = os.environ.get("MCP_SEARCH_ENDPOINT", "https://api.tavily.com/search")
API_KEY = os.environ.get("TAVILY_API_KEY")

@tool
def web_search(query: str) -> str:
    """
    Real web search using MCP-compatible API.
    """
    payload = {
        "api_key": API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 5
    }

    response = requests.post(MCP_SEARCH_ENDPOINT, json=payload, timeout=15)
    response.raise_for_status()

    results = response.json().get("results", [])

    if not results:
        return "No relevant information found."

    content = []
    for r in results:
        content.append(f"- {r.get('title')}: {r.get('content')}")

    return "\n".join(content)
