"""class to connect to tavily websearch tool"""
from typing import Optional
from pydantic import BaseModel
from tavily import TavilyClient
from .tavily_config import TavilyWebSearchConfig

class SearchResult(BaseModel):
    """Tavily search result."""
    url: str
    title: str
    content: str
    score: float
    raw_content: Optional[str] = None
    id: str

class TavilyResponse(BaseModel):
    """Tavily web search response."""
    query: str
    follow_up_questions: Optional[list[str]] = None
    answer: Optional[str] = None
    images: list[str]
    results: list[SearchResult]
    response_time: float
    request_id: str

class TavilyWebSearch:
    """web search tool using tavily"""
    def __init__(self,
                 config: TavilyWebSearchConfig) -> None:
        self.config = config
        self.client = TavilyClient(self.config.api_key)

    def search_in_web(self, message: str) -> TavilyResponse:
        """method to search in web using tavily
        Args:
            message (str): string to be searched
        Returns:
            TavilyResponse: parsed response from tavily
        """
        search_response = self.client.search(
            query = message,
            search_depth = str(self.config.search_depth),
        )

        return TavilyResponse.model_validate(search_response)