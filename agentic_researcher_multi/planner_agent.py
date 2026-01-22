import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

planner_llm = ChatOpenAI(
    model=os.environ.get("PLANNER_MODEL", "gpt-4o-mini"),
    temperature=0
)

def plan_tasks(goal: str) -> list[str]:
    prompt = f"""
You are a planning agent.

GOAL:
{goal}

Create a SHORT, ORDERED task list.
Rules:
- Tasks must be information-gathering or report-writing
- Each task MUST be solvable using search or writing
- Maximum 4 tasks
- No generic tasks like "organize", "review", "finalize"

Return ONLY a numbered list.
"""
    response = planner_llm.invoke(prompt)
    lines = response.content.split("\n")

    tasks = []
    for line in lines:
        if line.strip() and line[0].isdigit():
            tasks.append(line.split(".", 1)[1].strip())

    return tasks


def review_progress(collected_info: str, goal: str) -> str:
    prompt = f"""
You are reviewing task execution.

GOAL:
{goal}

COLLECTED INFORMATION:
{collected_info}


Answer STRICTLY with one word:
- FINISH → if definition, frameworks, pros & cons are present
- REPLAN → if any section is missing
"""
    response = planner_llm.invoke(prompt)
    return response.content.strip()