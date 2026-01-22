from agent import build_agent
from dotenv import load_dotenv
load_dotenv()

GOAL = """
Research Agentic AI frameworks and generate a markdown report covering:
- What Agentic AI is
- Key frameworks
- Pros and Cons
"""

agent = build_agent()

result = agent.invoke(
    {"input": GOAL}
)

print("\n✅ FINAL OUTPUT:\n")
print(result["output"])
