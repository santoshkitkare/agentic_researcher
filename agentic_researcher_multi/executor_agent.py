import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools import web_search, write_report

load_dotenv()

def build_executor(include_writer=False):
    llm = ChatOpenAI(
        model=os.environ.get("EXECUTOR_MODEL", "gpt-4o-mini"),
        temperature=0
    )

    tools = [web_search]
    if include_writer:
        tools.append(write_report)
        
    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3
    )

