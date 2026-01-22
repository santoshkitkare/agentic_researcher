from planner_agent import plan_tasks, review_progress
from executor_agent import build_executor
from supervisor_agent import review_plan, review_execution

GOAL = """
Research Agentic AI frameworks and generate a markdown report covering:
- What Agentic AI is
- Key frameworks
- Pros and Cons
"""

GOAL = """Create a Django learning roadmap from beginner to advanced,
including a sample production-grade project."""
MAX_PLANNER_RETRIES = 2
collected_info = ""

progress = {
    "definition": False,
    "frameworks": False,
    "pros": False,
    "cons": False
}

def is_ready_to_finish(progress: dict) -> bool:
    return all(progress.values())

for attempt in range(MAX_PLANNER_RETRIES):
    print(f"\n🧠 PLANNER ROUND {attempt + 1}\n")

    print("\n🧠 PLANNER AGENT THINKING...\n")
    tasks = plan_tasks(GOAL)
    
    supervisor_decision = review_plan(tasks, GOAL)
    print("\n🧠 SUPERVISOR DECISION:", supervisor_decision)
    
    if supervisor_decision == "STOP":
        print("🛑 Supervisor stopped execution.")
        break

    if supervisor_decision == "REPLAN":
        print("🔁 Supervisor requested replanning.")
        continue
    
    if supervisor_decision != "APPROVE_PLAN":
        print("⚠️ Unknown supervisor decision, stopping.")
        break

    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

    executor = build_executor()
    print("\n⚙️ EXECUTOR AGENT RUNNING...\n")

    for task in tasks:
        print(f"\n▶ Executing task: {task}")
        result = executor.invoke({"input": task})
        collected_info += "\n" + result["output"]

    # 4️⃣ Supervisor validates execution completeness
    execution_decision = review_execution(collected_info, GOAL)
    print("\n🧠 SUPERVISOR EXECUTION REVIEW:", execution_decision)

    if execution_decision != "APPROVE_WRITE":
        print("🔁 Supervisor rejected output, replanning.")
        continue

    # 5️⃣ Write final report (real file write)
    print("\n🧠 Writing final report to report.md")

    writer = build_executor(include_writer=True)
    writer.invoke({
        "input": f"""
Write a FINAL markdown report using ONLY the information below.
Do NOT perform any research.
Do NOT add new facts.

INFORMATION:
{collected_info}
    """
    })

    print("\n✅ Report successfully written. Workflow complete.")
    break

    print("\n✅ Multi-agent workflow completed.")
