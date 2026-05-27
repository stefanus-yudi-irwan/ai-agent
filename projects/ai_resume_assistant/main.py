from src.tool_registry import Tools
from src.resume_ai import ResumeAI
import gradio as gr
from dotenv import load_dotenv
import os

load_dotenv(override=True)
NOTIFICATION_TOKEN = os.getenv("NOTIFICATION_TOKEN")
NOTIFICATION_USER = os.getenv("NOTIFICATION_USER")
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
USER_NAME = os.getenv("USER_NAME")
FILES_PATH = os.getenv("FILES_PATH")

tool_engine = Tools(token = NOTIFICATION_TOKEN,
                    user = NOTIFICATION_USER,
                    url = NOTIFICATION_URL)

resume_ai = ResumeAI(openai_api_key = OPENAI_API_KEY,
                    model = OPENAI_MODEL,
                    persona_name = USER_NAME,
                    files_path = FILES_PATH,
                    tools = tool_engine)
                    
if __name__ == "__main__":
    gr.ChatInterface(resume_ai.chat, type="messages").launch()
