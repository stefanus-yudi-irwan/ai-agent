"""unit test for smtp"""
from unittest import TestCase
from unittest.mock import patch, Mock

import smtplib

from email_sender.smtp import (
    SMTPEmailSender,
    SMTPSenderConfig,
    SMTPEmailSenderError,
)


class UnitTestSMPT(TestCase):
    """test suite for smtp email sender"""

    def setUp(self) -> None:
        self.config = SMTPSenderConfig(
            smtp_server="test-server",
            app_password="test-password",
            sender_email="test@gmail.com",
        )

        self.smtp_sender = SMTPEmailSender(
            config=self.config
        )

    @patch("email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email(self, mock_smtp: Mock) -> None:
        """test email is successfully sent"""

        mock_server = mock_smtp.return_value.__enter__.return_value

        self.smtp_sender.send_email(
            to="receiver@gmail.com",
            subject="Test Subject",
            text_body="This is a test email.",
            html_body="<h1>This is a test email.</h1>",
        )

        # Verify SMTP connection
        mock_smtp.assert_called_once_with(
            "test-server",
            587,
        )

        # Verify TLS
        mock_server.starttls.assert_called_once_with()

        # Verify authentication
        mock_server.login.assert_called_once_with(
            "test@gmail.com",
            "test-password",
        )

        # Verify email was sent
        mock_server.send_message.assert_called_once()

    @patch("email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_error_authentication(
        self,
        mock_smtp: Mock,
    ) -> None:
        """test SMTP authentication error"""

        mock_server = mock_smtp.return_value.__enter__.return_value

        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(
            535,
            b"Authentication failed",
        )

        with self.assertRaises(SMTPEmailSenderError) as context:
            self.smtp_sender.send_email(
                to="receiver@gmail.com",
                subject="Test Subject",
                text_body="This is a test email.",
                html_body="<h1>This is a test email.</h1>",
            )

        self.assertEqual(
            str(context.exception),
            "SMTP authentication failed.",
        )

        self.assertIsInstance(
            context.exception.__cause__,
            smtplib.SMTPAuthenticationError,
        )

        mock_server.starttls.assert_called_once_with()
        mock_server.login.assert_called_once_with(
            "test@gmail.com",
            "test-password",
        )

        mock_server.send_message.assert_not_called()

    @patch("email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_error_recipient(
        self,
        mock_smtp: Mock,
    ) -> None:
        """test SMTP recipient refused error"""

        mock_server = mock_smtp.return_value.__enter__.return_value

        mock_server.send_message.side_effect = (
            smtplib.SMTPRecipientsRefused(
                {
                    "receiver@gmail.com": (
                        550,
                        b"Recipient refused",
                    )
                }
            )
        )

        with self.assertRaises(SMTPEmailSenderError) as context:
            self.smtp_sender.send_email(
                to="receiver@gmail.com",
                subject="Test Subject",
                text_body="This is a test email.",
                html_body="<h1>This is a test email.</h1>",
            )

        self.assertEqual(
            str(context.exception),
            "SMTP recipient refused: receiver@gmail.com",
        )

        self.assertIsInstance(
            context.exception.__cause__,
            smtplib.SMTPRecipientsRefused,
        )

        mock_server.starttls.assert_called_once_with()
        mock_server.login.assert_called_once_with(
            "test@gmail.com",
            "test-password",
        )

        mock_server.send_message.assert_called_once()

    @patch("email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_error_exception(
        self,
        mock_smtp: Mock,
    ) -> None:
        """test general SMTP exception"""

        mock_server = mock_smtp.return_value.__enter__.return_value

        mock_server.send_message.side_effect = smtplib.SMTPException(
            "SMTP server error"
        )

        with self.assertRaises(SMTPEmailSenderError) as context:
            self.smtp_sender.send_email(
                to="receiver@gmail.com",
                subject="Test Subject",
                text_body="This is a test email.",
                html_body="<h1>This is a test email.</h1>",
            )

        self.assertIn(
            "SMTP error while sending email",
            str(context.exception),
        )

        self.assertIn(
            "SMTP server error",
            str(context.exception),
        )

        self.assertIsInstance(
            context.exception.__cause__,
            smtplib.SMTPException,
        )

        mock_server.starttls.assert_called_once_with()
        mock_server.login.assert_called_once_with(
            "test@gmail.com",
            "test-password",
        )

        mock_server.send_message.assert_called_once()

    @patch("email_sender.smtp.smtp.smtplib.SMTP")
    def test_send_email_error_os_error(
        self,
        mock_smtp: Mock,
    ) -> None:
        """test SMTP connection OSError"""

        mock_smtp.side_effect = OSError(
            "Connection refused"
        )

        with self.assertRaises(SMTPEmailSenderError) as context:
            self.smtp_sender.send_email(
                to="receiver@gmail.com",
                subject="Test Subject",
                text_body="This is a test email.",
                html_body="<h1>This is a test email.</h1>",
            )

        self.assertIn(
            "SMTP connection error",
            str(context.exception),
        )

        self.assertIn(
            "Connection refused",
            str(context.exception),
        )

        self.assertIsInstance(
            context.exception.__cause__,
            OSError,
        )