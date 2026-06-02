"""
Script for email sender using sendgrid
"""
from loguru import logger
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Dict

class GridEmailSender:
    def __init__(self, 
                api_key: str,
                email_sender: str,
                email_receiver: str) -> None:
        self.sg = sendgrid.SendGridAPIClient(api_key = api_key)
        self.email_sender = Email(email_sender)
        self.email_receiver = To(email_receiver)
    
    def send_email(self,
                content: str,
                subject: str) -> Dict[str, int]:
        content_email = Content("text/plain", content)
        mail = Mail(self.email_sender, self.email_receiver, subject, content_email).get()
        response = self.sg.client.mail.send.post(request_body = mail)
        logger.info(f"RESPONSE STATUS CODE: {response.status_code}")
        return {"status": response.status_code}

    def send_html_email(self,
                        subject: str,
                        html_body: str) -> Dict[str, int]:
        content_email = Content("text/html", html_body)
        mail = Mail(self.email_sender, self.email_receiver, subject, content_email).get()
        response = self.sg.client.mail.send.post(request_body = mail)
        logger.info(f"RESPONSE STATUS CODE: {response.status_code}")
        return {"status": response.status_code}