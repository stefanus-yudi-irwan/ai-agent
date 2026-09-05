"""integration test for serper packages"""
import os
from unittest import TestCase
from dotenv import load_dotenv
from web_searcher.serper import SerperWebSearchConfig
from web_searcher.serper import SerperWebSearch

load_dotenv(override=True)

class IntegrationTestSerperWebSearch(TestCase):
    """test suite for serper web search"""

    def setUp(self) -> None:
        self.config = SerperWebSearchConfig(
            api_key= str(os.getenv("SERPER_API_KEY")),
            url= str(os.getenv("SERPER_URL")),
            geographic_preference= str(os.getenv("SERPER_GEOGRAPHIC_PREFERENCE")),
            language_preference= str(os.getenv("SERPER_LANGUAGE"))
        )

        self.serper = SerperWebSearch(
            config=self.config
        )

    def test_search_in_web(self) -> None:
        """test method search in web"""
        search_result = self.serper.search_in_web(message="The most demanding skill in 2027")
        self.assertIsNotNone(search_result)
        print(search_result)