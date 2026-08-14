"""class to connect to tavily websearch tool"""
from typing import Optional
from pydantic import BaseModel
from tavily import TavilyClient
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
    favicon: str
    images: list[Image]
    id: str

class AutoParameters(BaseModel):
    """tavily searching parameters"""
    topic: str
    search_depth: str

class Usage(BaseModel):
    """tavily creadit usage"""
    credits: int

class TavilyResponse(BaseModel):
    """data class to hose tavily response"""
    query: str
    answer: str
    images: list
    results: list[SearchResult]
    response_time: float
    auto_parameters: AutoParameters
    usage: Usage
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