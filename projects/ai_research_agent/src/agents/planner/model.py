"""planner agent response format"""
from pydantic import BaseModel, Field

class WebSearchItem(BaseModel):
    """class to contain item for websearch"""
    reason: str = Field(description="Your reasoning for why this search is imporant to the query")
    query: str = Field(description="The search term to use for the web search")

class WebSearchPlan(BaseModel):
    """class to contain plan for websearch"""
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")