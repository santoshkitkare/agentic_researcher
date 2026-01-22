import os
from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """
    Search for information about a topic.
    """
    q = query.lower()

    if "definition" in q or "what is" in q:
        return "Agentic AI systems autonomously plan, decide, and act using tools to achieve goals."

    if "framework" in q:
        return """
Key Agentic AI frameworks:
- LangChain: Tool-based agent orchestration
- AutoGPT: Autonomous task decomposition
- BabyAGI: Task queue–driven agents
- CrewAI: Role-based multi-agent systems
"""

    if "advantage" in q or "benefit" in q:
        return """
Benefits of Agentic AI:
- Autonomy
- Scalability
- Faster execution
- Reduced human intervention
"""

    if "disadvantage" in q or "challenge" in q or "risk" in q:
        return """
Challenges of Agentic AI:
- Hallucinations
- Safety risks
- Ethical concerns
- Cost unpredictability
"""

    if "application" in q or "use case" in q:
        return """
Applications of Agentic AI:
- Autonomous research agents
- Code assistants
- DevOps automation
- Customer support agents
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
