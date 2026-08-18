"""script for planner agent"""
import os
from agents import Agent, Runner
from .planner_config import WebSearchPlan, WebSearchItem, SEARCH_NUMBER

class PlannerAgent:
    """class for planner agent"""
    def __init__(self) -> None:
        self.agent = Agent(
            name = "planner-agent",
            instructions = f"""
            You are a research assistant. Given a user query, come up with a set of web searches
            to perform to best answer the query. Output {SEARCH_NUMBER} terms to query for.
            """,
            model = os.getenv("OPENAI_MODEL"),
            output_type = WebSearchPlan
        )

    async def agentic_plan(self, query: str) -> list[WebSearchItem]:
        """method to plan search using AI"""
        result = await Runner.run(self.agent, f"Query: {query}") 
        return result.final_output.searches