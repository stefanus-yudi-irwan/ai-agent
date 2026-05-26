"""Script for tool registry
"""
from typing import List, Any
import json
import requests
from loguru import logger

class Notification:
    """Class to enable notification via pushover
    """
    def __init__(self, token: str, user: str, url: str) -> None:
        """Class initialization
        """
        self.token = token
        self.user = user
        self.url = url
    
    def push(self, message: str) -> None:
        """Function to push notification via pushover
        """
        requests.post(
            self.url,
            data = {
                "token": self.token,
                "user": self.user,
                "message": message
            }
        )

class Tools:
    """Class to manage tools
    """
    def __init__(self, token: str, user: str, url: str) -> None:
        """Initialization class for AI tools
        """
        self.notification_engine = Notification(token, user, url)
        self.tools = [{"type": "function", "function": self.record_user_details_schema()},
                      {"type": "function", "function": self.record_unknown_question_schema()}]

    # =========================
    # Actual tool functions
    # =========================

    def record_user_details(self, 
                            email: str = "EMAIL-NOT-PROVIDED",
                            name: str = "NAME-NOT-PROVIDED",
                            notes: str = "NOTES-NOT-PROVIDED"):
        """Tools to record user email, name, and notes
        """
        self.notification_engine.push(f"Recording interest from {name} with email {email} and notes {notes}")
        return {"recorded": "ok"}
    
    def record_unknown_question(self, 
                                question: str):
        """Tools to record if there are unanswered question
        """
        self.notification_engine.push(f"Recording {question} asked that I couldn't answer")
        return {"recorded": "ok"}

    # =========================
    # Tool Schemas
    # =========================
    def record_user_details_schema(self):
        """Schema for record user details tools
        """
        return {
                    "name": "record_user_details",
                    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "description": "The email address of this user"
                            },
                            "name": {
                                "type": "string",
                                "description": "The user's name, if they provided it"
                            },
                            "notes": {
                                "type": "string",
                                "description": "Any additional information about this conversation that's worth recording to give context"
                            }
                        },
                        "required": ["email"],
                        "additionalProperties": False
                    }
                }

    def record_unknown_question_schema(self):
        """Schema for record unknown question tools
        """
        return{
                    "name": "record_unknown_question",
                    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The question that couldn't be answered"
                            },
                        },
                        "required": ["question"],
                        "additionalProperties": False
                    }
                }

    # =========================
    # Tool Dispatcher
    # =========================
    def handle_tool_calls(self,
                        tool_calls: List[Any]):
        """Method to handle tool calls
        """
        results = []
        for tool_call in tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            logger.info(f"TOOL CALLED: {tool_name}")

            if tool_name == "record_user_details":
                result = self.record_user_details(**arguments)
            elif tool_name == "record_unknown_question":
                result = self.record_unknown_question(**arguments)
            else:
                result = {"recorded": "not ok"}
            
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        
        return results