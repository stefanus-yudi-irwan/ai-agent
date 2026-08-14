"""Tests for SendGrid email sender."""
from unittest import TestCase
from unittest.mock import MagicMock, patch
from .sendgrid import SendGridEmailSender
from .sendgrid_config import SendgridConfig

class SendGridEmailSenderTestSuite(TestCase):
    """Test suite for SendGridEmailSender."""

    def setUp(self) -> None:
        """set up test dependencies."""
        self.config = SendgridConfig(
            api_key="test-api-key",
            email_sender="sender@test.com",
        )

    def tearDown(self) -> None:
        """clean up test resources"""

    @patch("component.tools.email_sender.sendgrid.sendgrid.SendGridAPIClient")
    def test_send_email(self, mock_sendgrid_client: MagicMock) -> None:
        """test sending a plain-text email."""
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_sendgrid_client.return_value.client.mail.send.post.return_value = (
            mock_response
        )

        sender = SendGridEmailSender(
            config=self.config,
        )

        result = sender.send_email(
            content="Hello, this is a test.",
            subject="Test Email",
            email_receiver="receiver@test.com",
        )

        self.assertEqual(result, {"status": 202})

        mock_sendgrid_client.return_value.client.mail.send.post.assert_called_once()

    @patch("component.tools.email_sender.sendgrid.sendgrid.SendGridAPIClient")
    def test_send_html_email(self, mock_sendgrid_client: MagicMock) -> None:
        """test sending an HTML email."""
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_sendgrid_client.return_value.client.mail.send.post.return_value = (
            mock_response
        )

        sender = SendGridEmailSender(
            config=self.config,
        )

        result = sender.send_html_email(
            html_body="<h1>Hello</h1>",
            subject="Test HTML Email",
            email_receiver="receiver@test.com",
        )

        self.assertEqual(result,{"status": 202})

        mock_sendgrid_client.return_value.client.mail.send.post.assert_called_once()