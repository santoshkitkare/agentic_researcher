from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from tools import web_search, write_report

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
