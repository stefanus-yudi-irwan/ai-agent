"""integration test for tavily packages"""
import os
from unittest import TestCase
from dotenv import load_dotenv
from web_searcher.tavily import TavilyWebSearchConfig
from web_searcher.tavily import TavilyWebSearch

load_dotenv(override=True)

class IntegrationTestTavilyWebSearch(TestCase):
    """test suite for tavily web searc"""

    def setUp(self) -> None:
        self.config = TavilyWebSearchConfig(
            api_key = str(os.getenv("TAVILY_API_KEY")),
            search_depth = "basic"
        )

        self.tavily = TavilyWebSearch(
            config = self.config
        )

    def test_search_in_web(self) -> None:
        """test method search in web"""
        search_result = self.tavily.search_in_web(message="The most demanding skill in 2027")
        self.assertIsNotNone(search_result)
        print(search_result)