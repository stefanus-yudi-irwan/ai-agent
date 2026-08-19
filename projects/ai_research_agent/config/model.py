"""config loader"""
from pydantic import BaseModel

class AgentConfig(BaseModel):
    """basic configuration for agents"""
    name: str
    instructions: str
    model: str

class AgentsConfig(BaseModel):
    """all agent configuration"""
    planner: AgentConfig
    searcher: AgentConfig
    writer: AgentConfig
    emailer: AgentConfig

class TavilyConfig(BaseModel):
    """configuration for tavily search"""
    TAVILY_API_KEY: str

class SMTPConfig(BaseModel):
    """configuration for SMTP config"""
    EMAIL_SMTP_SERVER: str
    EMAIL_APP_PASSWORD: str
    EMAIL_ADDRESS_SENDER: str
    EMAIL_ADDRESS_RECEIVER: str

class ToolsConfig(BaseModel):
    """all tool configuration"""
    search: TavilyConfig
    email: SMTPConfig

class AppConfig(BaseModel):
    """all app element configuration"""
    agent: AgentsConfig
    tool: ToolsConfig