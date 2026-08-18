"""script for search agent"""
import os
from dotenv import load_dotenv
from agents.model_settings import ModelSettings
from agents import Agent, Runner, function_tool
from .tavily_client import TavilyWebSearch, TavilyResponse
from .tavily_config import TavilyWebSearchConfig, TavilySearchDepth

load_dotenv(override=True)

tavily_config = TavilyWebSearchConfig(
    api_key = os.getenv("TAVILY_API_KEY"),
    search_depth = TavilySearchDepth.BASIC
)
tavily = TavilyWebSearch(config = tavily_config)

@function_tool
def tavily_search(search_message: str) -> TavilyResponse:
    """search a string through website
    Args:
        search_message (str): string to be searched in web
    Returns:
        TavilyResponse: Tasearch result in Tavily format
    """
    search_response = tavily.search_in_web(message = search_message)
    return search_response

class SearchAgent:
    """class for searching agent"""
    def __init__(self) -> None:
        self.agent = Agent(
            name = "search-agent",
            instructions = """
                You are a research assistant. Given a search term, you search the web for that term and 
                produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
                Capture the main points and be succinct. Reply only with the summary.
                """,
            model = os.getenv("OPENAI_MODEL"),
            model_settings = ModelSettings(tool_choice="required"),
            tools = [tavily_search]
        )

    async def agentic_search(self, search_task: str) -> str:
        """method to perform searching using AI"""
        result = await Runner.run(self.agent, search_task) 
        return result.final_output