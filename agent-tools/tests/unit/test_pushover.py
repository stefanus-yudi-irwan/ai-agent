"""unit test for pushover package"""
from unittest import TestCase
from unittest.mock import patch, Mock
import requests
from notification_pusher.pushover import (
    PushOverConfig,
    PushOverClient,
    PushOverClientError
)


class UnitTestPushover(TestCase):
    """test suite for pushover"""

    def setUp(self) -> None:
        self.config = PushOverConfig(
            token= "test-token",
            user = "test-user",
            url = "test-url"
        )

        self.pushover = PushOverClient(config=self.config)

    @patch("notification_pusher.pushover.pushover.requests.post")
    def test_push_message(self, mock_post) -> None:
        """test method push message"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": 1,
            "request": "647d2300-702c-4b38-8b2f-d56326ae460b"
        }
        mock_post.return_value = mock_response

        push_result = self.pushover.push_message(
            message = "test-message",
            title = "test-title",
            priority = 1
        )

        self.assertEqual(push_result, {
            "status": 1,
            "request": "647d2300-702c-4b38-8b2f-d56326ae460b"
        })

        mock_post.assert_called_once_with(
            self.pushover.config.url,
            data = {
                "token": self.pushover.config.token,
                "user": self.pushover.config.user,
                "message": "test-message",
                "title": "test-title",
                "priority": 1,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()

    @patch("notification_pusher.pushover.pushover.requests.post")
    def test_push_message_empty(self, mock_post) -> None:
        """test method push message when message empty"""
        with self.assertRaises(PushOverClientError) as context:
            self.pushover.push_message(message="")

        self.assertEqual(
            str(context.exception),
            "notification message cannot be empty"
        )

        mock_post.assert_not_called()

    @patch("notification_pusher.pushover.pushover.requests.post")
    def test_push_message_error(self, mock_post) -> None:
        """test method push message when error"""
        mock_response = Mock()

        http_error = requests.exceptions.HTTPError(
            "400 Client Error"
        )
        http_error.response = Mock(status_code=400)

        mock_response.raise_for_status.side_effect = http_error
        mock_post.return_value = mock_response

        with self.assertRaises(PushOverClientError) as context:
            self.pushover.push_message(
                message="test-message"
            )

        self.assertEqual(
            str(context.exception),
            "pushover API returned HTTP 400"
        )

        mock_response.raise_for_status.assert_called_once()