import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

llm = ChatOpenAI(
    model=os.environ.get("SUPERVISOR_MODEL", "gpt-4o-mini"),
    temperature=0
)

def review_plan(tasks: list[str], goal: str) -> str:
    prompt = f"""
You are a SUPERVISOR agent.

GOAL:
{goal}

PLANNED TASKS:
{chr(10).join(tasks)}

Rules:
- Tasks must be research-only
- No writing / compiling / formatting tasks
- Maximum 4 tasks
- Tasks must directly support the goal
- Prefer fewer tasks when using real tools
- Avoid redundant or overlapping tasks
- Stop once sufficient information is collected

Decide ONE:
- APPROVE_PLAN
- REPLAN
- STOP

Return ONLY the decision word.
"""
    response = llm.invoke(prompt)
    return response.content.strip()


# REVIEW_PROMPT = PromptTemplate(
#     input_variables=["goal", "content"],
#     template="""
# You are a strict SUPERVISOR AGENT.

# Your task is to determine whether the execution output
# fully satisfies the given GOAL.

# GOAL:
# {goal}

# EXECUTION OUTPUT:
# {content}

# Steps to follow:
# 1. Infer the key requirements and expected deliverables from the GOAL.
# 2. Check whether the output satisfies ALL inferred requirements.
# 3. Ensure the output is:
#    - Relevant to the goal
#    - Sufficiently complete
#    - Suitable for a final user-facing deliverable

# Rules:
# - Minor wording or formatting issues are acceptable.
# - Missing major requirements is NOT acceptable.
# - Do NOT assume domain-specific sections unless required by the goal.

# Respond with EXACTLY ONE token:
# - APPROVE_WRITE
# - REPLAN

# Do NOT explain your reasoning.
# Do NOT add extra text.
# """
# )

SUPERVISOR_PROMPT = PromptTemplate(
    input_variables=["goal", "content"],
    template="""You are a Supervisor Agent.

USER GOAL:
{goal}

COLLECTED INFORMATION:
{collected_info}

TASK:
Evaluate whether the collected information is sufficient to write a final report
that fully satisfies the USER GOAL.

Criteria:
- All major concepts required by the goal are covered
- Information is relevant and not repetitive
- No critical sections implied by the goal are missing

IMPORTANT:
- Do NOT require the report to already be written
- Do NOT suggest improvements
- Only decide readiness

Return ONLY one of:
- APPROVE_WRITE
- REPLAN
"""
)


def review_execution(collected_info: str, goal: str) -> str:
    """
    Supervisor reviews executor output and decides whether
    the system is ready to write the final report.
    """
    review_chain = REVIEW_PROMPT | llm
    decision = review_chain.invoke({
        "goal": goal,
        "content": collected_info
    }).content.strip()

    if decision not in {"APPROVE_WRITE", "REPLAN"}:
        # Fail-safe: never allow accidental approval
        return "REPLAN"

    return decision