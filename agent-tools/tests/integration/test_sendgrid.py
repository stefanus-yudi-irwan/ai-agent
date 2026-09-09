"""integration test for sendgrid packages"""
import os
from unittest import TestCase
from dotenv import load_dotenv
from email_sender.sendgrid import (
    SendGridEmailSender,
    SendGridConfig,
)

load_dotenv(override=True)

class IntegrationTestSendgridEmailSender(TestCase):
    """test suite for sendgrid email sender"""

    def setUp(self) -> None:
        self.config = SendGridConfig(
            api_key=str(os.getenv("SENDGRID_API_KEY")),
            email_sender=str(os.getenv("SENDGRID_EMAIL_SENDER"))
        )

        self.sendgrid = SendGridEmailSender(
            config = self.config
        )

    def test_send_email(self) -> None:
        """test sendgrid for email"""
        test_subject = "Integration Test – SendGrid Email Sender"
        test_content = """
        Hello,

        This is an integration test email for the SendGridEmailSender component.

        The purpose of this email is to verify that:

        The SendGrid API connection is working.
        The email sender address is configured correctly.
        The recipient address is configured correctly.
        The email subject and content are delivered correctly.

        This message was generated automatically as part of the integration test.

        Best regards,
        AI Agent Integration Test
        """
        results = self.sendgrid.send_email(
            content = test_content,
            subject = test_subject,
            email_receiver = "yudi.stefanus22@gmail.com"
        )
        print(results)
        

    def test_send_html_email(self) -> None:
        """test sendgrid for html email"""
        test_subject = "Integration Test – SendGrid HTML Email Sender"
        test_html_content = """
        <html> <body> <h2>SendGrid Integration Test</h2>

        <p>
            This is an integration test email for the
            <strong>SendGridEmailSender</strong> component.
        </p>

        <p>The purpose of this test is to verify that:</p>

        <ul>
            <li>The SendGrid API connection is working.</li>
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
        results = self.sendgrid.send_email(
            content = test_html_content,
            subject = test_subject,
            email_receiver = "yudi.stefanus22@gmail.com"
        )
        print(results)