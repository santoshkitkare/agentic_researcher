from planner_agent import plan_tasks, review_progress
from executor_agent import build_executor

GOAL = """
Research Agentic AI frameworks and generate a markdown report covering:
- What Agentic AI is
- Key frameworks
- Pros and Cons
"""
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

    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

    executor = build_executor()
    print("\n⚙️ EXECUTOR AGENT RUNNING...\n")

    for task in tasks:
        print(f"\n▶ Executing task: {task}")
        result = executor.invoke({"input": task})
        collected_info += "\n" + result["output"]

        if "define" in task.lower():
            progress["definition"] = True
        elif "framework" in task.lower():
            progress["frameworks"] = True
        elif "pros" in task.lower():
            progress["pros"] = True
        elif "cons" in task.lower():
            progress["cons"] = True
            
        if is_ready_to_finish(progress):
            print("\n🧠 All required sections collected.")
            print("🧠 Writing final report.")

            writer = build_executor(include_writer=True)

            writer.invoke({
                "input": f"""
            Write a FINAL markdown report using ONLY the information below.
            Do NOT perform any research.

            INFORMATION:
            {collected_info}
            """
            })
            break

    print("\n✅ Multi-agent workflow completed.")
