"""script for pushover configuration"""
from dataclasses import dataclass

@dataclass
class PushOverConfig:
    """class for pushover notification"""
    token: str
    user: str
    url: str