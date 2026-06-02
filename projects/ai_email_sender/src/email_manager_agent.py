"""
Script for email manager agent
"""
from agents import Agent, set_default_openai_client
from openai import AsyncOpenAI
from pydantic import BaseModel

class EmailManagerAgent:
    def __init__(self,
                model: str,
                api_key: str) -> None:
        self.client = AsyncOpenAI(api_key = api_key)
        set_default_openai_client(self.client)
        self.model = model

    def create_subject_writer_agent(self):
        agent_name = "email_subject_writer"
        agent_identity = "You can write a subject for a cold sales email. \
            You are given a message and you need to write a subject for an email that is likely to get a response."
        agent_command = "Writer a subject for a cold sales email"

        subject_writer = Agent(
            name = agent_name,
            instructions = agent_identity,
            model = self.model
        )

        subject_writer_tool = subject_writer.as_tool(tool_name = agent_name,
                                                    tool_description = agent_command)

        return subject_writer_tool

    def create_html_formatter_agent(self):
        agent_name = "html_email_formatter"
        agent_identity = "You can convert a text email body to an HTML email body. \
            You are given a text email body which might have some markdown \
            and you need to convert it to an HTML email body with simple, clear, compelling layout and design."
        agent_command = "Convert a text email body to an HTML email body"

        html_formatter = Agent(
            name = agent_name,
            instructions = agent_identity,
            model = self.model
        )

        html_formatter_tool = html_formatter.as_tool(tool_name = agent_name,
                                                    tool_description = agent_command) 
        
        return html_formatter_tool

    def create_email_manager_agent(self, email_sender_tool):

        subject_writer_agent_tool = self.create_subject_writer_agent()
        html_formatter_agent_tool = self.create_html_formatter_agent()

        agent_name = "email_manager"
        agent_identity = "You are an email formatter and sender. You receive the body of an email to be sent. \
            You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. \
            Finally, you use the send_html_email tool to send the email with the subject and HTML body."
        agent_command = ""

        email_manager_agent = Agent(
            name = agent_name,
            instructions = agent_identity,
            model = self.model,
            tools = [subject_writer_agent_tool, html_formatter_agent_tool, email_sender_tool],
            handoff_description = "Convert an email to HTML and send it"
        )

        return email_manager_agent