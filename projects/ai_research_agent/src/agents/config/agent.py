"""configuration for agents"""
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """configuration for agents"""
    name: str
    instructions: str
    model: str