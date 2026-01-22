class ResearchAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = []

    def decide(self, goal: str, observation: str) -> str:
        prompt = f"""
You are an autonomous research agent.

GOAL:
{goal}

PREVIOUS OBSERVATION:
{observation}

Decide the next action.

You must respond with EXACTLY one of the following formats:

SEARCH: <search query>
WRITE: <final markdown report>
FINISH
"""
        return self.llm(prompt)

    def observe(self, result: str):
        self.memory.append(result)
