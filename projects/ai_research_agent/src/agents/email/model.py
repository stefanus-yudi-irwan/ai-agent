"""emailer agent response format"""
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class EmailAgentResponse(BaseModel, Generic[T]):
    """result format from email agent"""
    final_output: str
    email_result: T