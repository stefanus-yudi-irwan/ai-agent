"""
Script for email writer agent
"""
from agents import Agent, set_default_openai_client
from openai import AsyncOpenAI
from pydantic import BaseModel

class EmailWriterAgent:
    def __init__(self,
                model: str,
                api_key: str) -> None:
        self.client = AsyncOpenAI(api_key = api_key)
        set_default_openai_client(self.client)
        self.model = model

    def create_professional_sales_agent(self):
        agent_name = "professional_sales_agent"
        agent_identity = "You are a sales agent working for ComplAI, \
                a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
                You write professional, serious cold emails."
        agent_command = "Write a cold sales email"

        professional_sales_agent = Agent(
            name = agent_name,
            instructions = agent_identity,
            model = self.model
        )

        professional_sales_agent_tool = professional_sales_agent.as_tool(tool_name = agent_name,
                                                                        tool_description = agent_command)
        
        return professional_sales_agent_tool

    def create_engaging_sales_agent(self):
        agent_name = "engaging_sales_agent"
        agent_identity = "You are a humorous, engaging sales agent working for ComplAI, \
                a company that provides a SaaS tool for ensuring SOC2 compliance an preparing for audits, powered by AI. \
                You write witty, engaging cold emails that are likely to get a response"
        agent_command = "Write a cold sales email"

        engaging_sales_agent = Agent(
            name = agent_name,
            instructions = agent_identity,
            model = self.model
        )

        engaging_sales_agent_tool = engaging_sales_agent.as_tool(tool_name = agent_name,
                                                                tool_description = agent_command)

        return engaging_sales_agent_tool

    def create_busy_sales_agent(self):
        agent_name = "busy_sales_agent"
        agent_identity = "You are a humorous, engaging sales agent working for ComplAI, \
                a company that provides a SaaS tool for ensuring SOC2 compliance an preparing for audits, powered by AI. \
                You write concise, to the point cold emails."
        agent_command = "Write a cold sales email"

        busy_sales_agent = Agent(
            name = agent_name,
            instructions = agent_identity,
            model = self.model
        )

        busy_sales_agent_tool = busy_sales_agent.as_tool(tool_name = agent_name, 
                                                        tool_description = agent_command)

        return busy_sales_agent_tool

    def create_email_sales_tools(self):
        professional_sales_agent_tool = self.create_professional_sales_agent()
        engaging_sales_agent_tool = self.create_engaging_sales_agent()
        busy_sales_agent_tool = self.create_busy_sales_agent()

        email_writer_tools = [professional_sales_agent_tool,
                            engaging_sales_agent_tool,
                            busy_sales_agent_tool]

        return email_writer_tools   