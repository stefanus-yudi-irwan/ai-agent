"""llm client class"""
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from .config import LLMConfig

class LLMClient:
    """class to connect to LLM
    """
    def __init__(self, config: LLMConfig) -> None:
        """class initialization
        Args:
            config (dict): class configuration
        """
        self.llm = OpenAI(api_key = config.api_key, base_url = config.base_url)
        self.model = config.model

    def create_llm_message(self, message: str) -> list[ChatCompletionMessageParam]:
        """method to create llm message
        Args:
            message (str): message to be given to LLM
        Returns:
            Iterable[ChatCompletionMessageParam]: formatted message for LLM input
        """
        llm_message: list[ChatCompletionMessageParam] = [
            {"role": "user", "content": message}
        ]
        return llm_message
       
    def ask_llm(self, message: str) -> str | None:
        """method to ask to llm
        Args:
            message (str): message to be given to LLM
        Returns:
            str | None: response string from LLM
        """
        llm_message = self.create_llm_message(message)
        llm_response = self.llm.chat.completions.create(
            model = self.model,
            messages = llm_message
        )
        response = llm_response.choices[0].message.content
        return response