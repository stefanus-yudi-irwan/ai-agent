"""script for email sender agent"""
import os
from agents import Agent, function_tool, Runner
from .smtp_config import SMTPSenderConfig
from .smtp import SMTPEmailSender

smtp_config = SMTPSenderConfig(
    smtp_server = os.getenv("EMAIL_SMTP_SERVER"),
    app_password = os.getenv("EMAIL_APP_PASSWORD"),
    sender_email = os.getenv("EMAIL_ADDRESS")
)

smtp_sender = SMTPEmailSender(config = smtp_config)

@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """Send out an email with the given subject and body to all sales prospects
    Args:
        subject (str): The subject of the email
        text_body (str): The body of the email as plain text
        html_body (str): The HTML body of the email
    """
    smtp_sender.send_email(to = os.getenv("EMAIL_ADDRESS"),
                           subject=subject,
                           text_body=text_body,
                           html_body=html_body)
    return "Email sent sucessfully"

class EmailerAgent:
    """class for emailer agent"""
    def __init__(self) -> None:
        self.agent = Agent(
            name = "emailer-agent",
            instructions = """
            You are provided with a detailed report. Use your tool to send an email, converting the report into
            a clean, well presented HTML email with an appropriate subject line.
            """,
            model = os.getenv("OPENAI_MODEL"),
            tools = [send_email_tool]
        )

    async def agentic_send(self, input_message: str) -> str:
        """method to send email using AI"""
        result = await Runner.run(self.agent, input_message) 
        return result.final_output