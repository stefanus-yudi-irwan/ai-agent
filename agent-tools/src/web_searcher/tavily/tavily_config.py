"""configuration for tavily web search tool"""
from dataclasses import dataclass
from typing import Literal

SearchDepth = Literal[
    "basic",
    "advanced",
    "fast",
    "ultra-fast"
]

@dataclass
class TavilyWebSearchConfig:
    """configuration for tavily websearch"""
    api_key: str
    search_depth: SearchDepth = "basic"
