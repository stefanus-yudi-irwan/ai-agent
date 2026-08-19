"""agentic ai for web search"""
from typing import Generic, TypeVar
from agents.model_settings import ModelSettings
from agents import Agent, Runner, Tool, ToolCallOutputItem
from src.agents.config.agent import AgentConfig
from .model import SearchAgentResponse

T = TypeVar("T")

class SearchAgent(Generic[T]):
    """class for web search agent"""
    def __init__(self, config: AgentConfig, tool: Tool) -> None:
        """agent initialization
        Args:
            config (AgentConfig): agent config
            tool (Tool): search tool used by agent
        """
        self.agent = Agent(
            name = config.name,
            instructions = config.instructions,
            model = config.model,
            model_settings = ModelSettings(tool_choice="required"),
            tools = [tool]
        )

    async def search(self, search_words: str) -> SearchAgentResponse[T]:
        """method for agent using search tool
        Args:
            search_words (str): words that will be used by search tool
        Raises:
            RuntimeError: error if the search tool didn't response
        Returns:
            SearchAgentResponse[T]: response from the agent
        """
        response = await Runner.run(self.agent, search_words)
        search_result = None
        for item in response.new_items:
            if isinstance(item, ToolCallOutputItem):
                search_result = item.output
                break

        if search_result is None:
            raise RuntimeError("Search tool did not return a result")

        return SearchAgentResponse(
            summary = response.final_output,
            search_result = search_result
        )