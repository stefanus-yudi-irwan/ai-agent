"""script for sendgrid email sender"""
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from .sendgrid_config import SendgridConfig

class SendGridEmailSender:
    """class for email sender using sendgrid"""

    def __init__(self, config: SendgridConfig) -> None:
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
        email_receiver = To(email = email_receiver)
        mail = Mail(self.email_sender, email_receiver, subject, content_email).get()
        response = self.sg.client.mail.send.post(request_body = mail)
        return {"status": response.status_code}

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
        email_receiver = To(email = email_receiver)
        mail = Mail(self.email_sender, email_receiver, subject, content_email).get()
        response = self.sg.client.mail.send.post(request_body = mail)
        return {"status": response.status_code}