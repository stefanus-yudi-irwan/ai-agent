"""
Script for name checker agent
"""
from agents import Agent, Runner, GuardrailFunctionOutput, input_guardrail, set_default_openai_client
from pydantic import BaseModel
from openai import AsyncOpenAI

class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

class NameCheckAgent:
    def __init__(self,
                model: str,
                api_key: str) -> None:
        self.client = AsyncOpenAI(api_key = api_key)
        set_default_openai_client(self.client)
        self.model = model

        agent_name = "name_check",
        agent_identity = "Check if the user is including someone's personal name in what they want you to do."
        self.name_check_agent = Agent(
            name = agent_name,
            instructions = agent_identity,
            output_type = NameCheckOutput,
            model = self.model
        )

    async def guardrail_against_name(self, ctx, agent, message) -> NameCheckOutput:
        result = await Runner.run(self.name_check_agent, message, context=ctx.context)
        is_name_in_message = result.final_output.is_name_in_message
        return GuardrailFunctionOutput(output_info={"found_name": result.final_output}, tripwire_triggered=is_name_in_message)