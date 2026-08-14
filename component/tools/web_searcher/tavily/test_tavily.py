"""tests for Tavily web search tool"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
from .tavily import TavilyWebSearch, TavilyResponse
from .tavily_config import TavilyWebSearchConfig, TavilySearchDepth


class TestTavilyWebSearch(TestCase):
    """test suite for tavily web search"""

    def setUp(self) -> None:
        self.config = TavilyWebSearchConfig(
            api_key="test-api-key",
            search_depth=TavilySearchDepth.BASIC,
        )

    @patch("component.tools.web_searcher.tavily.tavily.TavilyClient")
    def test_init(self, mock_tavily_client: MagicMock) -> None:
        TavilyWebSearch(self.config)

        mock_tavily_client.assert_called_once_with(
            "test-api-key"
        )

    @patch("component.tools.web_searcher.tavily.tavily.TavilyClient")
    def test_search_in_web(
        self,
        mock_tavily_client: MagicMock,
    ) -> None:
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
                    "favicon": "https://example.com/favicon.png",
                    "images": [
                        {
                            "url": "https://example.com/messi.png",
                            "description": "Lionel Messi",
                        }
                    ],
                    "id": "result-001",
                }
            ],
            "response_time": "1.67",
            "auto_parameters": {
                "topic": "general",
                "search_depth": "basic",
            },
            "usage": {
                "credits": 1,
            },
            "request_id": "request-001",
        }

        tavily = TavilyWebSearch(self.config)

        result = tavily.search_in_web(
            "Who is Leo Messi?"
        )

        # Verify Tavily API was called correctly
        mock_client.search.assert_called_once_with(
            query="Who is Leo Messi?",
            search_depth="basic",
        )

        # Verify response type
        self.assertIsInstance(
            result,
            TavilyResponse,
        )

        # Verify response fields
        self.assertEqual(
            result.query,
            "Who is Leo Messi?",
        )

        self.assertEqual(
            result.answer,
            "Lionel Messi is an Argentine footballer.",
        )

        self.assertEqual(
            result.response_time,
            1.67,
        )

        self.assertEqual(
            result.request_id,
            "request-001",
        )

        # Verify nested result
        self.assertEqual(
            len(result.results),
            1,
        )

        search_result = result.results[0]

        self.assertEqual(
            search_result.title,
            "Lionel Messi Facts",
        )

        self.assertEqual(
            search_result.score,
            0.81,
        )

        self.assertEqual(
            search_result.id,
            "result-001",
        )

        # Verify nested image
        self.assertEqual(
            len(search_result.images),
            1,
        )

        self.assertEqual(
            search_result.images[0].url,
            "https://example.com/messi.png",
        )

        # Verify nested parameters
        self.assertEqual(
            result.auto_parameters.topic,
            "general",
        )

        self.assertEqual(
            result.auto_parameters.search_depth,
            "basic",
        )

        # Verify usage
        self.assertEqual(
            result.usage.credits,
            1,
        )