"""configuration for tavily web search tool"""
from dataclasses import dataclass
from enum import StrEnum

class TavilySearchDepth(StrEnum):
    """registered tavily search depth"""
    ULTRA_FAST = "ultra-fast"
    BASIC = "basic"
    ADVANCED = "advanced"
    FAST = "fast" 

@dataclass
class TavilyWebSearchConfig:
    """configuration for tavily websearch"""
    api_key: str
    search_depth: TavilySearchDepth
