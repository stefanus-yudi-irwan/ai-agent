"""agentic ai for report writer"""
from agents import Agent, Runner
from src.agents.config.agent import AgentConfig
from .model import ReportData

class WriterAgent:
    """class for writer agent"""
    def __init__(self, config: AgentConfig) -> None:
        """agent initialization
        Args:
            config (AgentConfig): agent config
        """
        self.agent = Agent(
            name = config.name,
            instructions = config.instructions,
            model = config.model,
            output_type = ReportData
        )

    async def write(self, reference: str) -> ReportData:
        """method to write report from reference data
        Args:
            reference (str): reference from search result
        Returns:
            ReportData: report of research result
        """
        result = await Runner.run(self.agent, reference) 
        return result.final_output