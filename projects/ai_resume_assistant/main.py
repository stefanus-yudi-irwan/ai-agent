import yaml
from src.tool_registry import Tools
from src.resume_ai import ResumeAI
import gradio as gr

with open("config/config.yaml", "r") as config_file:
    config_app = yaml.safe_load(config_file)

tool_engine = Tools(token = config_app["NOTIFICATION"]["TOKEN"],
                    user = config_app["NOTIFICATION"]["USER"],
                    url = config_app["NOTIFICATION"]["URL"])

resume_ai = ResumeAI(openai_api_key = config_app["OPENAI"]["API-KEY"],
                    model = config_app["OPENAI"]["MODEL"],
                    persona_name = config_app["USER"]["NAME"],
                    files_path = config_app["FILES"]["PATH"],
                    tools = tool_engine)
                    
if __name__ == "__main__":
    gr.ChatInterface(resume_ai.chat, type="messages").launch()
