"""agentic ai for email sender"""
from typing import Generic, TypeVar
from src.agents.config.agent import AgentConfig
from agents import Agent, Runner, Tool, ToolCallOutputItem
from .model import EmailAgentResponse

T = TypeVar("T")

class EmailerAgent(Generic[T]):
    """class for emailer agent"""
    def __init__(self, config: AgentConfig, tool: Tool) -> None:
        """agent initialization
        Args:
            config (AgentConfig): agent config
            tool (Tool): email tool used by agent
        """
        self.agent = Agent(
            name = config.name,
            instructions = config.instructions,
            model = config.model,
            tools = [tool]
        )

    async def send(self, email_text: str) -> EmailAgentResponse[T]:
        """method for agent using email tool

        Args:
            input_message (str): _description_

        Returns:
            EmailAgentResponse[T]: _description_
        """
        response = await Runner.run(self.agent, email_text) 

        email_result = None
        for item in response.new_items:
            if isinstance(item, ToolCallOutputItem):
                email_result = item.output
                break

        if email_result is None:
            raise RuntimeError("Email tool did not return a result")
        
        return EmailAgentResponse(
            final_output = response.final_output,
            email_result = email_result
        )