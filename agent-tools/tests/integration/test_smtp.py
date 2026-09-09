"""integration test for smtp packages"""
import os 
from unittest import TestCase
from dotenv import load_dotenv
from email_sender.smtp import (
    SMTPEmailSender,
    SMTPSenderConfig
)

load_dotenv(override=True)

class IntegrationTestSMTP(TestCase):
    """test suite for smpt email sender"""

    def setUp(self) -> None:
        self.config = SMTPSenderConfig(
            smtp_server = str(os.getenv("SMTP_SERVER")),
            app_password = str(os.getenv("SMTP_PASSWORD")),
            sender_email = str(os.getenv("SMTP_EMAIL_SENDER"))
        )

        self.smtp_sender = SMTPEmailSender(
            config = self.config
        )

    def test_send_email(self) -> None:
        """test smpt send email"""
        test_recipient = "yudi.stefanus22@gmail.com"
        test_subject = "Integration Test – SMTP Email Sender"
        test_content = """
        Hello,

        This is an integration test email for the SendGridEmailSender component.

        The purpose of this email is to verify that:

        The SMTP API connection is working.
        The email sender address is configured correctly.
        The recipient address is configured correctly.
        The email subject and content are delivered correctly.

        This message was generated automatically as part of the integration test.

        Best regards,
        AI Agent Integration Test
        """
        test_html_content = """
        <html> <body> <h2>SendGrid Integration Test</h2>

        <p>
            This is an integration test email for the
            <strong>SendGridEmailSender</strong> component.
        </p>

        <p>The purpose of this test is to verify that:</p>

        <ul>
            <li>The SMTP API connection is working.</li>
            <li>The sender address is configured correctly.</li>
            <li>The recipient address is configured correctly.</li>
            <li>The HTML email content is delivered correctly.</li>
        </ul>

        <p>
            If you received this email, the SendGrid HTML email integration
            test was successful.
        </p>

        <p>
            Best regards,<br>
            <strong>AI Agent Integration Test</strong>
        </p>

        </body> </html>
        """
        result = self.smtp_sender.send_email(
            to = test_recipient,
            subject = test_subject,
            text_body = test_content,
            html_body = test_html_content
        )
        self.assertTrue(result)