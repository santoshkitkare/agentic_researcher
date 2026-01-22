import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

from tools import write_report
from mcp_tools import web_search

load_dotenv()

EXECUTOR_PROMPT = PromptTemplate.from_template("""
You are an Executor Agent.

You execute ONE task at a time.

AVAILABLE TOOLS:
{tools}

Tool names:
{tool_names}

CRITICAL TOOL RULES:
- NEVER call tools using parentheses
- ALWAYS use:
  Action: web_search
  Action Input: <query>

TASK:
{input}

{agent_scratchpad}
""")

def build_executor(include_writer=False):
    llm = ChatOpenAI(
        model=os.environ.get("EXECUTOR_MODEL", "gpt-4o-mini"),
        temperature=0
    )

    tools = [web_search]
    if include_writer:
        tools.append(write_report)

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=EXECUTOR_PROMPT
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=4
    )
