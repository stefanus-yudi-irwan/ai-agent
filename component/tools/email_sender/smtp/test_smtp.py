"""Tests for SMTP email sender"""
from email.message import EmailMessage
from unittest import TestCase
from unittest.mock import MagicMock, patch
from smtp.smtp import SMTPEmailSender
from smtp.smtp_config import SMTPSenderConfig

class TestSMTPEmailSender(TestCase):
    """test suite for SMTP email sender"""

    def setUp(self) -> None:
        self.config = SMTPSenderConfig(
            sender_email="sender@example.com",
            app_password="app-password",
            smtp_server="smtp.example.com",
        )

        self.sender = SMTPEmailSender(self.config)

    @patch("component.tools.email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email(self, mock_smtp: MagicMock) -> None:
        mock_server = mock_smtp.return_value.__enter__.return_value

        self.sender.send_email(
            to="recipient@example.com",
            subject="Test Subject",
            text_body="This is a plain text email.",
            html_body="<h1>This is an HTML email.</h1>",
        )

        # SMTP connection
        mock_smtp.assert_called_once_with(
            "smtp.example.com",
            587,
        )

        # TLS
        mock_server.starttls.assert_called_once_with()

        # Authentication
        mock_server.login.assert_called_once_with(
            "sender@example.com",
            "app-password",
        )

        # Email sending
        mock_server.send_message.assert_called_once()

        # Verify the generated email
        email = mock_server.send_message.call_args.args[0]

        self.assertIsInstance(email, EmailMessage)
        self.assertEqual(email["From"], "sender@example.com")
        self.assertEqual(email["To"], "recipient@example.com")
        self.assertEqual(email["Subject"], "Test Subject")

    @patch("component.tools.email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_contains_plain_text_and_html(
        self,
        mock_smtp: MagicMock,
    ) -> None:
        mock_server = mock_smtp.return_value.__enter__.return_value

        self.sender.send_email(
            to="recipient@example.com",
            subject="Test Subject",
            text_body="Plain text content",
            html_body="<h1>HTML content</h1>",
        )

        email = mock_server.send_message.call_args.args[0]

        self.assertTrue(email.is_multipart())
        self.assertEqual(email.get_content_type(), "multipart/alternative")

        payload = email.get_payload()

        self.assertEqual(len(payload), 2)

        self.assertEqual(
            payload[0].get_content_type(),
            "text/plain",
        )
        self.assertEqual(
            payload[0].get_content().strip(),
            "Plain text content",
        )

        self.assertEqual(
            payload[1].get_content_type(),
            "text/html",
        )
        self.assertEqual(
            payload[1].get_content().strip(),
            "<h1>HTML content</h1>",
        )

    @patch("component.tools.email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_uses_configured_sender(
        self,
        mock_smtp: MagicMock,
    ) -> None:
        mock_server = mock_smtp.return_value.__enter__.return_value

        self.sender.send_email(
            to="another@example.com",
            subject="Subject",
            text_body="Text",
            html_body="<p>HTML</p>",
        )

        email = mock_server.send_message.call_args.args[0]

        self.assertEqual(
            email["From"],
            self.config.sender_email,
        )

    @patch("component.tools.email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_uses_recipient(
        self,
        mock_smtp: MagicMock,
    ) -> None:
        mock_server = mock_smtp.return_value.__enter__.return_value

        self.sender.send_email(
            to="recipient@example.com",
            subject="Subject",
            text_body="Text",
            html_body="<p>HTML</p>",
        )

        email = mock_server.send_message.call_args.args[0]

        self.assertEqual(
            email["To"],
            "recipient@example.com",
        )

    @patch("component.tools.email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_propagates_smtp_error(
        self,
        mock_smtp: MagicMock,
    ) -> None:
        mock_server = mock_smtp.return_value.__enter__.return_value

        mock_server.send_message.side_effect = Exception(
            "SMTP send failed"
        )

        with self.assertRaises(Exception) as context:
            self.sender.send_email(
                to="recipient@example.com",
                subject="Subject",
                text_body="Text",
                html_body="<p>HTML</p>",
            )

        self.assertEqual(
            str(context.exception),
            "SMTP send failed",
        )