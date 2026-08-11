"""llm client configuration"""
from dataclasses import dataclass
from enum import StrEnum

class LLMBaseURL(StrEnum):
    """registered llm provider and its base url"""
    OPENAI = "https://api.openai.com/v1"
    ANTHROPIC = "https://api.anthropic.com/v1/"
    DEEPSEEK = "https://api.deepseek.com/v1"
    GEMINI = "https://generativelanguage.googleapis.com/v1beta/openai/"
    GROQ = "https://api.groq.com/openai/v1"
    GROK = "https://api.x.ai/v1"
    OPENROUTER = "https://openrouter.ai/api/v1"

class LLMModel(StrEnum):
    """registered llm model"""
    GPT54NANO = "gpt-5.4-nano"
    GPT41NANO = "gpt-4.1-nano"
    CLAUDESONNET46 = "claude-sonnet-4-6"
    GEMINI31FLASHLITE = "gemini-3.1-flash-lite"
    DEEPSEEKV4FLASH = "deepseek-v4-flash"
    GPTOSS120B = "openai/gpt-oss-120b"
    KIMIK26 = "moonshotai/kimi-k2.6"
 
@dataclass(frozen=True)
class LLMConfig:
    """configuration for LLM"""
    base_url: LLMBaseURL
    model: LLMModel
    api_key: str