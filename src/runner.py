from agent import build_agent, evaluate_confidence
from dotenv import load_dotenv
load_dotenv()

GOAL = """
Research Agentic AI frameworks and generate a markdown report covering:
- What Agentic AI is
- Key frameworks
- Pros and Cons
"""

agent = build_agent()

collected_info = ""
CONFIDENCE_THRESHOLD = 0.75

for step in range(5):
    print(f"\n--- Step {step + 1} ---")

    result = agent.invoke({"input": GOAL})
    output = result["output"]

    collected_info += "\n" + output

    confidence = evaluate_confidence(collected_info)
    print(f"Confidence score: {confidence}")

    if confidence >= CONFIDENCE_THRESHOLD:
        print("\n✅ Confidence threshold reached. Stopping agent.")
        break

print("\n✅ FINAL OUTPUT:\n")
print(result["output"])
