"""
Script for Sales Manager Agent
"""
from typing import Callable
from agents import Agent, set_default_openai_client 
from openai import AsyncOpenAI

class SalesManagerAgent:
    """AI Agent to send email
    """
    def __init__(self,
                api_key: str,
                model_name: str) -> None:
        self.client = AsyncOpenAI(api_key = api_key)
        set_default_openai_client(self.client)
        self.model = model_name
    
    def create_sales_manager_agent(self, 
                                email_writer_tools: list,
                                email_manager_agent: Agent,
                                guardrail_function: Callable) -> Agent:

        agent_name = "sales_manager"
        agent_identity = """
            You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools. 
            Follow these steps carefully:
            1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
            2. Evaluate and Select: Review the drafts and choose the single best email using your judgement of which one is most effective.
            You can use the tools multiple times if you're not satisfied with the results from the first try.
            3. Handoff for Sending: Pass ONLY the winning email draft to the 'email_manager' agent. The Email Manager will take care of formatting and sending.
            Crucial Rules:
            - You must use the sales agent tools to generate the drafts - do not write them yourself.
            - You must send ONE email using the send_email tool - never more than one.
            """
        agent_command = ""

        sales_manager_agent = Agent(
            name = agent_name,
            instructions = agent_identity,
            model = self.model,
            tools = email_writer_tools,
            handoffs = email_manager_agent,
            input_guardrails = [guardrail_function],
        )

        return sales_manager_agent