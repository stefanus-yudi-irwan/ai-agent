"""smtp tools package"""
from .smtp_config import SMTPSenderConfig
from .smtp import SMTPEmailSender, SMTPEmailSenderError

__all__ = [
    "SMTPSenderConfig",
    "SMTPEmailSender",
    "SMTPEmailSenderError"
]