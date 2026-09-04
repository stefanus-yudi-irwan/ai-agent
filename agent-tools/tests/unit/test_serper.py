"""unit test for serper packages"""
from unittest import TestCase
from unittest.mock import patch, Mock
from web_searcher.serper import SerperWebSearchConfig
from web_searcher.serper import SerperWebSearch

class UnitTestSerperWebSearch(TestCase):
    """test suite for serper web search"""

    def setUp(self) -> None:
        self.config = SerperWebSearchConfig(
            api_key = "test-api-key",
            url = "test-url",
            geographic_preference = "test-geographic-preference",
            language_preference = "test-language-preference"
        )

        self.serper = SerperWebSearch(
            config=self.config
        )

    @patch("web_searcher.serper.serper.requests.post")
    def test_search_in_web(self, mock_post) -> None:
        """test method search in web"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "organic":[
                {
                    "snippet": "Python is a programming language."
                },
                {
                    "snippet": "Python is widely used in AI."
                }
            ]
        }
        mock_post.return_value = mock_response

        search_result = self.serper.search_in_web(message="Python programming")
        self.assertEqual(
            search_result,
            "Python is a programming language.\n\n"
            "Python is widely used in AI."
        )