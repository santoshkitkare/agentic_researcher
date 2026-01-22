def web_search(query: str) -> str:
    # Mock search (real API later)
    return f"""
Agentic AI frameworks include:
- LangChain
- AutoGPT
- BabyAGI
- CrewAI

Each enables autonomous decision-making via tools.
"""

def write_report(content: str):
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(content)
