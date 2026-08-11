"""test for llm client"""
from unittest import TestCase
from unittest.mock import MagicMock
from .config import LLMConfig, LLMBaseURL, LLMModel
from .llm import LLMClient

class LLMClientTestSuite(TestCase):
    """test suite for LLM client"""
    def setUp(self) -> None:
        """set up test dependencies"""

        self.config = LLMConfig(
            base_url=LLMBaseURL.OPENAI,
            model=LLMModel.GPT41NANO,
            api_key="test-api-key",
        )

        self.llm_client = LLMClient(
            config=self.config,
        )

    def tearDown(self) -> None:
        """clean up test resources"""

    def test_create_llm_message(self) -> None:
        """test creating an LLM message."""
        message = "Hello, world!"

        llm_message = self.llm_client.create_llm_message(
            message = message
        )

        self.assertEqual(llm_message,[{"role": "user", "content": message}])

    def test_ask_llm(self) -> None:
        """test asking the llm"""
        llm_response = MagicMock()
        llm_response.choices[0].message.content = "Hello! How can I help you?"

        self.llm_client.llm.chat.completions.create = MagicMock(
            return_value=llm_response,
        )

        response = self.llm_client.ask_llm(message="Hello")

        self.assertEqual(response, "Hello! How can I help you?")

        self.llm_client.llm.chat.completions.create.assert_called_once_with(
            model=self.llm_client.model,
            messages=[{"role": "user", "content": "Hello"}])