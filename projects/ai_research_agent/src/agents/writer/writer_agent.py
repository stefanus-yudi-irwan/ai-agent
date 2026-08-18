"""script for writer agent"""
import os
from agents import Agent, Runner
from .writer_config import ReportData

class WriterAgent:
    """class for writer agent"""
    def __init__(self) -> None:
        self.agent = Agent(
            name = "writer-agent",
            instructions = """
                You are a senior researcher tasked with writing a cohesive report for a research query.
                You will be provided with the original query, and some research.
                Generate a comprehensive report based on the research and the query.
                The final output should be in markdown format, and it should be lengthy and detailed. Aim 
                for 5-10 pages of content, at least 1000 words.
                """,
            model = os.getenv("OPENAI_MODEL"),
            output_type = ReportData
        )

    async def agentic_write(self, input_message: str) -> ReportData:
        """method to plan search using AI"""
        result = await Runner.run(self.agent, input_message) 
        return result.final_output