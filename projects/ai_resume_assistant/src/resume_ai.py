"""Script for resume AI
"""
from anyio.abc import AnyByteStream
from openai import OpenAI
import json
from pypdf import PdfReader
from typing import List, Any
from loguru import logger

class ResumeAI:
    """Class for interacting with open ai
    """
    def __init__(self,
                openai_api_key: str,
                persona_name: str,
                files_path: str,
                model: str,
                tools: Any):
        """Initiate resume ai class
        """
        self.openai = OpenAI(api_key = openai_api_key)
        self.persona_name = persona_name
        self.model = model
        self.tools = tools
        
        reader = PdfReader(files_path)
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text

    def system_prompt(self):
        system_prompt = f"You are acting as {self.persona_name}. You are answering questions on {self.persona_name}'s resume, \
            particularly questions related to {self.persona_name}'s career, background, skills and experience. \
            Your responsibility is to represent {self.persona_name} for interactions on the website as faithfully as possible. \
            You are given a summary of {self.persona_name}'s resume which you can use to answer questions. \
            Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer \
            even if it's about something trivial or unrelated to career. \
            If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your \
            record_user_details tool. "
        system_prompt += f"\n\n##Resume: \n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.persona_name}"
        return system_prompt

    def chat(self,
            message: str,
            history: str) -> None:
        """Main method to chat with AI
        """
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model = self.model,
                                                        messages=messages,
                                                        tools=self.tools.tools)
            finish_reason = response.choices[0].finish_reason
            logger.info(f"FINISH REASON: {finish_reason}")

            if finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.tools.handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content