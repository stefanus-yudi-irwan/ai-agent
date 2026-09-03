"""test for serper web search tool"""
import os
from unittest import TestCase
from dotenv import load_dotenv
from serper.serper_config import SerperWebSearchConfig
from serper.serper import SerperWebSearch

load_dotenv(override=True)

class TestSerperWebSearch(TestCase):
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