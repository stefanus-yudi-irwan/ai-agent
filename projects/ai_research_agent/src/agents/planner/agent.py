"""agentic ai for search planner"""
from agents import Agent, Runner
from src.agents.config.agent import AgentConfig
from .model import WebSearchItem, WebSearchPlan

class PlannerAgent:
    """class for planner agent"""
    def __init__(self, config: AgentConfig) -> None:
        """agent initialization
        Args:
            config (AgentConfig): agent config
        """
        self.agent = Agent(
            name = config.name,
            instructions = config.instructions,
            model = config.model,
            output_type = WebSearchPlan
        )

    async def plan(self, topic: str) -> list[WebSearchItem]:
        """function to produce search plans
        Args:
            topic (str): topic to be search
        Returns:
            list[WebSearchItem]: list of search item
        """
        response = await Runner.run(self.agent, f"Topic: {topic}") 
        return response.final_output.searches