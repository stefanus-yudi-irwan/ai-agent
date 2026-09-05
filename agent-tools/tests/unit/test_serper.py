"""unit test for serper packages"""
from unittest import TestCase
from unittest.mock import patch, Mock
import requests
from web_searcher.serper import SerperWebSearchConfig
from web_searcher.serper import SerperWebSearch
from web_searcher.serper import SerperWebSearchError

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

        search_result = self.serper.search_in_web(message="python programming")
        self.assertEqual(
            search_result,
            "Python is a programming language.\n\n"
            "Python is widely used in AI."
        )

    @patch("web_searcher.serper.serper.requests.post")
    def test_search_timeout(self, mock_post) -> None:
        """test method search in web when timeout"""
        mock_post.side_effect = requests.exceptions.Timeout()

        with self.assertRaises(SerperWebSearchError) as context:
            self.serper.search_in_web("python programming")

        self.assertEqual(
            str(context.exception),
            "request to serper API timed out"
        )

    @patch("web_searcher.serper.serper.requests.post")
    def test_search_connection_error(self, mock_post) -> None:
        """test method search in web when connection error"""
        mock_post.side_effect = requests.exceptions.ConnectionError()

        with self.assertRaises(SerperWebSearchError) as context:
            self.serper.search_in_web("python programming")

        self.assertEqual(
            str(context.exception),
            "could not connect to serper API"
        )

    @patch("web_searcher.serper.serper.requests.post")
    def test_search_http_error(self, mock_post) -> None:
        """test method search in web when http error"""
        mock_response = mock_post.return_value
        http_error = requests.exceptions.HTTPError(
            "401 Client Error"
        )
        http_error.response = mock_response
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = http_error

        with self.assertRaises(SerperWebSearchError) as context:
            self.serper.search_in_web("python programming")

        self.assertEqual(
            str(context.exception),
            "serper API returned HTTP 401"
        )

    @patch("web_searcher.serper.serper.requests.post")
    def test_search_invalid_json(self, mock_post) -> None:
        """test method search in web then json decode error"""
        mock_response = mock_post.return_value
        json_error = requests.exceptions.JSONDecodeError(
            "Invalid JSON", "invalid json", 0
        )
        mock_response.json.side_effect = json_error

        with self.assertRaises(SerperWebSearchError) as context:
            self.serper.search_in_web("python programming")

        self.assertEqual(
            str(context.exception),
            "serper API returned an invalid JSON response"
        )