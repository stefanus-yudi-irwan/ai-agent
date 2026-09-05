"""class to connect to tavily websearch tool"""
from typing import Optional
from pydantic import BaseModel, ValidationError
from tavily import TavilyClient
from loguru import logger
from .tavily_config import TavilyWebSearchConfig

class Image(BaseModel):
    """tavily image response data"""
    url: str
    description: str

class SearchResult(BaseModel):
    """tavily search results"""
    title: str
    url: str
    content: str
    score: float
    raw_content: Optional[str]
    id: str

class TavilyResponse(BaseModel):
    """data class to hose tavily response"""
    query: str
    answer: Optional[str]
    images: list[str]
    results: list[SearchResult]
    response_time: float
    request_id: str

class TavilyWebSearchError(Exception):
    """Raise when a Tavily web search fails"""

class TavilyWebSearch:
    """web search tool using tavily"""
    def __init__(self, config: TavilyWebSearchConfig) -> None:
        self.config = config
        self.client = TavilyClient(self.config.api_key)

    def search_in_web(self, message: str) -> TavilyResponse:
        """method to search in web using tavily
        Args:
            message (str): string to be searched
        Returns:
            TavilyResponse: parsed response from tavily
        """
        try:
            search_response = self.client.search(
                query = message,
                search_depth = self.config.search_depth,
            )
        except Exception as e:
            error = TavilyWebSearchError(f"Tavily API request failed: {e}") 
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e

        try:
            return TavilyResponse.model_validate(search_response)
        except ValidationError as e:
            error = TavilyWebSearchError(f"Invalid response from Tavily: {e}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e