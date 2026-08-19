"""class to sent email via smtp"""
import smtplib
from email.message import EmailMessage
from agents import function_tool
from .config import SMTPSenderConfig
from .model import SMTPResponse

class SMTPEmailSender:
    """class to send email using smtp"""
    def __init__(self, config: SMTPSenderConfig) -> None:
        self.config = config

    def send_email(self,
                   subject: str,
                   text_body: str,
                   html_body: str) -> SMTPResponse:
        """method to send email
        Args:
            subject (str): email subject
            text_body (str): body text of the email in string
            html_body (str): body text of the email using html
        """
        email = EmailMessage()
        email["From"] = self.config.sender_email
        email["To"] = self.config.receiver_email
        email["Subject"] = subject
        email.set_content(text_body)
        email.add_alternative(html_body, subtype="html")

        try:
            with smtplib.SMTP(self.config.smtp_server, 587) as server:
                server.starttls()
                server.login(self.config.sender_email, self.config.app_password)
                failed = server.send_message(email)
                if failed:
                    return SMTPResponse(
                        success=False,
                        error=f"Failed recipients: {failed}" 
                    )

                return SMTPResponse(success=True)

        except smtplib.SMTPException as error:
            return SMTPResponse(
                success=False,
                error=str(error)
            )

    def send(self,
             subject: str,
             body: str,
             html: str) -> SMTPResponse:
        """method to send email
        Args:
            subject (str): email subject
            text_body (str): body text of the email in string
            html_body (str): body text of the email using html
        """
        return self.send_email(subject, body, html)