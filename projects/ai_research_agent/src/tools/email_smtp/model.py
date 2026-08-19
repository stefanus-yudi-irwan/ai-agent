"""smtp email sender response format"""
from pydantic import BaseModel

class SMTPResponse(BaseModel):
    """class to contain reponse from the SMTP server"""
    success: bool
    error: str | None = None