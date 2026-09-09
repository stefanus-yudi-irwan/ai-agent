"""unit test for sendgrid"""
from unittest import TestCase
from unittest.mock import patch, MagicMock
from email_sender.sendgrid import SendGridConfig
from email_sender.sendgrid import SendGridEmailSender
from email_sender.sendgrid import SendGridEmailSenderError
from python_http_client.exceptions import HTTPError

class UnitTestSendgrid(TestCase):
    """test suite for sendgrid email sender"""

    @patch("email_sender.sendgrid.sendgrid.sendgrid.SendGridAPIClient")
    def setUp(self, mock_sendgrid_client) -> None:
        self.config = SendGridConfig(
            api_key = "test-api-key",
            email_sender = "you@gmail.com"
        )

        self.mock_sg = mock_sendgrid_client.return_value

        self.sendgrid = SendGridEmailSender(
            config = self.config
        )

    @patch("email_sender.sendgrid.sendgrid.sendgrid.SendGridAPIClient")
    def test_initialization_creates_sendgrid_client(self, mock_sendgrid_client):
        """test SendGrid API client is created correctly"""
        SendGridEmailSender(self.config)
        mock_sendgrid_client.assert_called_once_with(
            api_key="test-api-key"
        )

    def test_send_email_success(self):
        """test send_email successfully sends an email"""

        expected_result = {
            "status_code": 202,
        }
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.sendgrid.sg.client.mail.send.post.return_value = mock_response

        result = self.sendgrid.send_email(
            content="Hello, this is a test email",
            subject="Test Subject",
            email_receiver="receiver@example.com",
        )

        self.assertEqual(result, expected_result)

        self.sendgrid.sg.client.mail.send.post.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()

    def test_send_email_http_error(self) -> None: 
        """test send_email handles SendGrid HTTPError""" 
        mock_error_response = MagicMock()
        mock_error_response.code = 500
        mock_error_response.body = "SendGrid request failed"
        mock_error_response.headers = {}
        http_error = HTTPError(mock_error_response) 
        self.sendgrid.sg.client.mail.send.post.side_effect = http_error

        with self.assertRaises(SendGridEmailSenderError) as context:
            self.sendgrid.send_email(
                content="Hello",
                subject="Test",
                email_receiver="receiver@example.com",
            ) 

        self.assertIn("SendGrid API error", str(context.exception))
        self.assertIsInstance(context.exception.__cause__, HTTPError)

    def test_send_email_unexpected_error(self):
        """test send_email handles unexpected errors"""

        unexpected_error = ValueError("Something unexpected happened")
        self.sendgrid.sg.client.mail.send.post.side_effect = unexpected_error

        with self.assertRaises(SendGridEmailSenderError) as context:
            self.sendgrid.send_email(
                content="Hello",
                subject="Test",
                email_receiver="receiver@example.com",
            )

        self.assertIn("Unexpected error while sending email", str(context.exception))
        self.assertIsInstance(context.exception.__cause__, ValueError)

    def test_send_email_html_success(self):
        """test send_email successfully sends an email"""

        expected_result = {
            "status_code": 202,
        }
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        self.sendgrid.sg.client.mail.send.post.return_value = mock_response

        result = self.sendgrid.send_html_email(
            html_body="<p>Hello, this is a test email</p>",
            subject="Test Subject",
            email_receiver="receiver@example.com",
        )

        self.assertEqual(result, expected_result)

        self.sendgrid.sg.client.mail.send.post.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()

    def test_send_email_html_http_error(self) -> None: 
        """test send_email handles SendGrid HTTPError""" 
        mock_error_response = MagicMock()
        mock_error_response.code = 500
        mock_error_response.body = "SendGrid request failed"
        mock_error_response.headers = {}
        http_error = HTTPError(mock_error_response) 
        self.sendgrid.sg.client.mail.send.post.side_effect = http_error

        with self.assertRaises(SendGridEmailSenderError) as context:
            self.sendgrid.send_html_email(
                html_body="<p>Hello</p>",
                subject="Test",
                email_receiver="receiver@example.com",
            ) 

        self.assertIn("SendGrid API error", str(context.exception))
        self.assertIsInstance(context.exception.__cause__, HTTPError)

    def test_send_email_html_unexpected_error(self):
        """test send_email handles unexpected errors"""

        unexpected_error = ValueError("Something unexpected happened")
        self.sendgrid.sg.client.mail.send.post.side_effect = unexpected_error

        with self.assertRaises(SendGridEmailSenderError) as context:
            self.sendgrid.send_html_email(
                html_body="<p>Hello</p>",
                subject="Test",
                email_receiver="receiver@example.com",
            )

        self.assertIn("Unexpected error while sending email", str(context.exception))
        self.assertIsInstance(context.exception.__cause__, ValueError)