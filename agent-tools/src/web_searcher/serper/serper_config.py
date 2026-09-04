"""configuration for serper web search tool"""
from dataclasses import dataclass

@dataclass
class SerperWebSearchConfig:
    """configuration for serper web search"""
    api_key: str
    url: str
    geographic_preference: str
    language_preference: str