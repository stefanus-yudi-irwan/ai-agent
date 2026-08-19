"""search agent reponse format"""
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class SearchAgentResponse(BaseModel, Generic[T]):
    """response format from search agent"""
    summary: str
    search_result: T