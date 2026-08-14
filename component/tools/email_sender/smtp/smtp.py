"""class to sent email via smtp"""
import smtplib
from email.message import EmailMessage
from .smtp_config import SMTPSenderConfig

class SMTPEmailSender:
    """class to send email using smtp"""
    def __init__(self, config: SMTPSenderConfig) -> None:
        self.config = config

    def send_email(self,
                   to: str,
                   subject: str,
                   text_body: str,
                   html_body: str) -> None:
        """method to send email
        Args:
            to (str): email address recipient
            subject (str): email subject
            text_body (str): body text of the email in string
            html_body (str): body text of the email using html
        """
        email = EmailMessage()
        email["From"] = self.config.sender_email
        email["To"] = to
        email["Subject"] = subject
        email.set_content(text_body)
        email.add_alternative(html_body, subtype="html")

        with smtplib.SMTP(self.config.smtp_server, 587) as server:
            server.starttls()
            server.login(self.config.sender_email, self.config.app_password)
            server.send_message(email)