"""class to connect to tavily websearch tool"""
from tavily import TavilyClient
from agents import function_tool
from .config import TavilyWebSearchConfig
from .model import TavilySearchResult, TavilyResponse

class TavilyWebSearch:
    """web search tool using tavily"""
    def __init__(self,
                 config: TavilyWebSearchConfig) -> None:
        self.config = config
        self.client = TavilyClient(self.config.api_key)

    def search_in_web(self, message: str) -> TavilySearchResult:
        """method to search in web using tavily
        Args:
            message (str): string to be searched
        Returns:
            TavilySearchResult: response from tavily search
        """
        try:
            search_response = self.client.search(
                query = message,
                search_depth = self.config.search_depth.value,
            )

            parsed_response = TavilyResponse.model_validate(search_response)

            return TavilySearchResult(
                success=True,
                response=parsed_response
            )

        except Exception as error:
            return TavilySearchResult(
                success=False,
                error=str(error)
            )

    def search(self, message: str) -> TavilySearchResult:
        """method to search in web using tavily
        Args:
            message (str): string to be searched
        Returns:
            TavilySearchResult: response from tavily search
        """
        return self.search_in_web(message)