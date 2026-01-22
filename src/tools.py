import os
from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """
    Search for information about a topic.
    """
    query = query.lower()

    if "what is" in query or "definition" in query:
        return """
Agentic AI refers to AI systems designed to autonomously plan,
decide, and execute actions using tools in order to achieve a goal.
"""

    if "framework" in query:
        return """
Popular Agentic AI frameworks include:
- LangChain
- AutoGPT
- BabyAGI
- CrewAI
"""

    if "pros" in query or "cons" in query:
        return """
Pros:
- Autonomy
- Task decomposition
- Reduced human intervention

Cons:
- Hallucinations
- Infinite loops
- Tool misuse
- Cost unpredictability
"""

    return "No relevant information found."

@tool
def write_report(content: str) -> str:
    """
    Write the final markdown report to a file.
    """
    os.makedirs("output", exist_ok=True)
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(content)
    return "Report written successfully."
