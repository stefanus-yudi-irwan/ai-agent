"""script for sendgrid configuration"""
from dataclasses import dataclass

@dataclass
class SendgridConfig:
    """class for sendgrid confuguration"""
    api_key: str
    email_sender: str
