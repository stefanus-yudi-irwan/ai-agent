import os
import asyncio
from agents import function_tool, input_guardrail, Runner, trace
from loguru import logger
from dotenv import load_dotenv
from openai import api_key
from projects.ai_email_sender.src import email_writer_agent
from src.sender import GridEmailSender
from src.sales_manager_agent import SalesManagerAgent
from src.email_manager_agent import EmailManagerAgent
from src.email_writer_agent import EmailWriterAgent
from src.name_checker_agent import NameCheckAgent
from typing import Dict

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_EMAIL_SENDER = os.getenv("SENDGRID_EMAIL_SENDER")
SENDGRID_EMAIL_RECEIVER = os.getenv("SENDGRID_EMAIL_RECEIVER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

logger.info("CONFIGURE EMAIL SENDER")
email_sender = GridEmailSender(api_key = SENDGRID_API_KEY,
                        email_sender = SENDGRID_EMAIL_SENDER,
                        email_receiver = SENDGRID_EMAIL_RECEIVER)

logger.info("CONFIGURE AGENTS")
name_checker_agent = NameCheckAgent(model = OPENAI_MODEL, api_key = OPENAI_API_KEY)
email_writer_agent = EmailWriterAgent(model = OPENAI_MODEL, api_key = OPENAI_API_KEY)
email_manager_agent = EmailManagerAgent(model = OPENAI_MODEL, api_key = OPENAI_API_KEY)
sales_manager_agent = SalesManagerAgent(model = OPENAI_MODEL, api_key = OPENAI_API_KEY)

logger.info("CREATE AGENTS INSTANCE")

@function_tool
def send_html_email(email_recipient: str, subject: str, html_body: str) -> Dict[str, int]:
    result = email_sender.send_html_email(email_recipient, subject, html_body)
    return result

@input_guardrail
async def guardrail_against_name(ctx, message):
    result = await name_checker_agent.guardrail_against_name(ctx, message)
    return result

email_writer_agent_instance = email_writer_agent.create_email_sales_tools()
email_manager_agent_instance = email_manager_agent.create_email_manager_agent(send_html_email)
sales_manager_agent_instance = sales_manager_agent.create_sales_manager_agent(
                                                email_writer_tools = email_writer_agent_instance,
                                                email_manager_agent = email_manager_agent_instance,
                                                guardrail_function = guardrail_against_name)

if __name__ == "__main__":
    async def main():
        message = "Send out a cold sales email addressed to Dear CEO from Head of Business Development"
        with trace("Protected Automated SDR"):
            result = await Runner.run(sales_manager_agent_instance, message)
        print(result.final_output)

    asyncio.run(main())