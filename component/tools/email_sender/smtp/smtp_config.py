"""config for smtp email sender"""
from dataclasses import dataclass

@dataclass
class SMTPSenderConfig:
    """class for smtp email sender config"""
    smtp_server: str
    app_password: str
    sender_email: str