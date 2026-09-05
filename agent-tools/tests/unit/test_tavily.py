"""unit test for tavily packages"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
from web_searcher.tavily import (
    TavilyWebSearchConfig,
    TavilyWebSearch,
    TavilyResponse,
    TavilyWebSearchError
)

class UnitTestTavilyWebSearch(TestCase):
    """test suite for tavily web searc"""

    def setUp(self) -> None:
        self.config = TavilyWebSearchConfig(
            api_key = "test-api-key",
            search_depth = "basic"
        )

    @patch("web_searcher.tavily.tavily.TavilyClient")
    def test_search_in_web(self, mock_tavily_client: MagicMock) -> None:
        """test method search in web"""
        mock_client = mock_tavily_client.return_value
        mock_client.search.return_value = {
            "query": "Who is Leo Messi?",
            "answer": "Lionel Messi is an Argentine footballer.",
            "images": [],
            "results": [
                {
                    "title": "Lionel Messi Facts",
                    "url": "https://example.com/messi",
                    "content": "Lionel Messi is an Argentine footballer.",
                    "score": 0.81,
                    "raw_content": None,
                    "id": "result-001",
                }
            ],
            "response_time": "1.67",
            "request_id": "request-001",
        }

        tavily_client = TavilyWebSearch(self.config)
        search_result = tavily_client.search_in_web("Who is Leo Messi?")

        mock_client.search.assert_called_once_with(
            query="Who is Leo Messi?",
            search_depth="basic"
        )

        self.assertIsInstance(
            search_result,
            TavilyResponse
        )

        self.assertEqual(
            search_result.answer, 
            "Lionel Messi is an Argentine footballer."
        )

        self.assertEqual(
            search_result.response_time,
            1.67,
        )

        self.assertEqual(
            search_result.request_id,
            "request-001",
        )

        self.assertEqual(
            len(search_result.results),
            1,
        )

        result_component = search_result.results[0]

        self.assertEqual(
            result_component.title,
            "Lionel Messi Facts",
        )

        self.assertEqual(
            result_component.score,
            0.81,
        )

        self.assertEqual(
            result_component.id,
            "result-001",
        )

    @patch("web_searcher.tavily.tavily.TavilyClient")
    def test_search_in_web_validation_error(self, mock_tavily_client: MagicMock) -> None:
        """test search in web when validation response error"""
        mock_client = mock_tavily_client.return_value
        mock_client.search.return_value = {
            "query": "Who is Leo Messi?",
            "answer": "Lionel Messi is an Argentine footballer.",
        }

        tavily_client = TavilyWebSearch(self.config)

        with self.assertRaises(TavilyWebSearchError) as context:
            tavily_client.search_in_web("Who is Leo Messi?")

        self.assertIn(
            "Invalid response from Tavily",
            str(context.exception),
        )

        mock_client.search.assert_called_once_with(
            query="Who is Leo Messi?",
            search_depth="basic",
        )

    @patch("web_searcher.tavily.tavily.TavilyClient")
    def test_search_in_web_call_error(self, mock_tavily_client: MagicMock) -> None:
        """test search in web when call error"""
        mock_client = mock_tavily_client.return_value
        mock_client.search.side_effect = Exception("Unauthorized: missing or invalid API key.")

        tavily_client = TavilyWebSearch(self.config)

        with self.assertRaises(TavilyWebSearchError) as context:
            tavily_client.search_in_web("Who is Leo Messi?")

        self.assertEqual(
            str(context.exception),
            "Tavily API request failed: "
            "Unauthorized: missing or invalid API key.",
        )

        mock_client.search.assert_called_once_with(
            query="Who is Leo Messi?",
            search_depth="basic",
        )