"""test for pushover notification tool"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
from .pushover import PushOverClient
from .pushover_config import PushOverConfig

class PushOverTestSuite(TestCase):
    """test suite for pushover"""
    def setUp(self) -> None:
        """set up test dependencies"""

        self.config = PushOverConfig(
            token = "test-token",
            user = "test-user",
            url = "test-url"
        )

        self.pusher = PushOverClient(
            config = self.config
        )

    def tearDown(self) -> None:
        """clean up test resources"""

    @patch("requests.post")
    def test_push_message(self, mock_post: MagicMock) -> None:
        """test pushing message"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = self.pusher.push_message(
            message="Test notification",
        )

        self.assertEqual(response, {"status": 200})

        mock_post.assert_called_once_with(
            "test-url",
            data={
                "token": "test-token",
                "user": "test-user",
                "message": "Test notification",
            },
            timeout=10,
        )

    def test_push_empty_message(self) -> None:
        """test pushing message if message empty"""
        with self.assertRaises(ValueError):
            self.pusher.push_message(message="")
