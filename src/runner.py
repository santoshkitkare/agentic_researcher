from agent import ResearchAgent
from tools import web_search, write_report
from llm import call_llm

GOAL = """
Research Agentic AI frameworks and generate a markdown report covering:
- What Agentic AI is
- Key frameworks
- Pros and Cons
"""

agent = ResearchAgent(call_llm)
observation = ""

MAX_STEPS = 5

for step in range(MAX_STEPS):
    print(f"\n--- Step {step + 1} ---")
    decision = agent.decide(GOAL, observation)
    print("Agent Decision:", decision)

    if decision.startswith("SEARCH"):
        query = decision.replace("SEARCH:", "").strip()
        observation = web_search(query)
        agent.observe(observation)

    elif decision.startswith("WRITE"):
        content = decision.replace("WRITE:", "").strip()
        write_report(content)
        print("\n✅ Report written to output/report.md")
        break

    elif decision.startswith("FINISH"):
        print("\n🛑 Agent decided to stop.")
        break
else:
    print("\n⚠️ Max steps reached. Agent stopped.")
