import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools import web_search, write_report
from dotenv import load_dotenv
load_dotenv()

confidence_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def evaluate_confidence(collected_info: str) -> float:
    prompt = f"""
You are evaluating whether enough information has been collected
to write a complete report.

Collected information:
{collected_info}

Rate confidence from 0 to 1.
Return ONLY a number.
"""
    response = confidence_llm.invoke(prompt)
    return float(response.content.strip())

reflection_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def reflect_on_progress(collected_info: str, goal: str) -> str:
    prompt = f"""
You are an AI reviewer.

GOAL:
{goal}

CURRENT COLLECTED INFORMATION:
{collected_info}

Critically analyze the progress.
Answer concisely:
- What is missing?
- What is weak or unclear?
- What should be done next?

Return a short reflection.
"""
    response = reflection_llm.invoke(prompt)
    return response.content.strip()

def build_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    tools = [web_search, write_report]

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5
    )

    return agent_executor
