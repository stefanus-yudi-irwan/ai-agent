"""class to sent email via smtp"""
import smtplib
from email.message import EmailMessage
from loguru import logger
from .smtp_config import SMTPSenderConfig

class SMTPEmailSenderError(Exception):
    """Raise error when SMPT email sender error"""

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

        try:
            with smtplib.SMTP(self.config.smtp_server, 587) as server:
                server.starttls()
                server.login(self.config.sender_email, self.config.app_password)
                server.send_message(email)

        except smtplib.SMTPAuthenticationError as e:
            error = SMTPEmailSenderError("SMTP authentication failed.")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e

        except smtplib.SMTPRecipientsRefused as e:
            error = SMTPEmailSenderError(f"SMTP recipient refused: {to}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e
        
        except smtplib.SMTPException as e:
            error = SMTPEmailSenderError(f"SMTP error while sending email: {e}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e

        except OSError as e:
            error = SMTPEmailSenderError(f"SMTP connection error: {e}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e
