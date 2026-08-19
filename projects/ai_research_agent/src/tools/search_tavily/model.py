"""tavily search response format"""
from pydantic import BaseModel

class SearchResult(BaseModel):
    """Tavily search result."""
    url: str
    title: str
    content: str
    score: float
    raw_content: str | None = None
    id: str

class TavilyResponse(BaseModel):
    """Tavily web search response."""
    query: str
    follow_up_questions: list[str] | None = None
    answer: str | None = None
    images: list[str]
    results: list[SearchResult]
    response_time: float
    request_id: str

class TavilySearchResult(BaseModel):
    """Tavily success or fail response"""
    success: bool
    response: TavilyResponse | None = None
    error: str | None = None