"""script for sendgrid email sender"""
import sendgrid
from python_http_client.exceptions import HTTPError
from loguru import logger
from sendgrid.helpers.mail import Mail, Email, To, Content
from .sendgrid_config import SendGridConfig

class SendGridEmailSenderError(Exception):
    """Raise error when sendgrid email sender get error"""

class SendGridEmailSender:
    """class for email sender using sendgrid"""

    def __init__(self, config: SendGridConfig) -> None:
        """class sendgrid initialization"""
        self.config = config
        self.sg = sendgrid.SendGridAPIClient(api_key = self.config.api_key)
        self.email_sender = Email(self.config.email_sender)
    
    def send_email(self,
                   content: str,
                   subject: str,
                   email_receiver: str) -> dict[str, int]:
        """method to send email in text
        Args:
            content (str): email content in text format
            subject (str): subject email
            email_receiver (str): email address receiver
        Returns:
            dict[str, int]: response status from http call
        """
        content_email = Content("text/plain", content)
        receiver = To(email = email_receiver)
        mail = Mail(self.email_sender, receiver, subject, content_email).get()

        try:
            response = self.sg.client.mail.send.post(request_body = mail)
            response.raise_for_status()
            results = response.json()
            return results

        except HTTPError as e:
            error = SendGridEmailSenderError(f"SendGrid API error: {e}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e
        
        except Exception as e:
            error = SendGridEmailSenderError( f"Unexpected error while sending email: {e}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e

    def send_html_email(self,
                        html_body: str,
                        subject: str,
                        email_receiver: str) -> dict[str, int]:
        """method to send email in html
        Args:
            html_body (str): email content with html format
            subject (str): subject email
        Returns:
            dict[str, int]: response status from http call
        """
        content_email = Content("text/html", html_body)
        receiver = To(email = email_receiver)
        mail = Mail(self.email_sender, receiver, subject, content_email).get()

        try:
            response = self.sg.client.mail.send.post(request_body = mail)
            response.raise_for_status()
            results = response.json()
            return results

        except HTTPError as e:
            error = SendGridEmailSenderError(f"SendGrid API error: {e}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e
        
        except Exception as e:
            error = SendGridEmailSenderError( f"Unexpected error while sending email: {e}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e