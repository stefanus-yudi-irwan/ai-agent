"""writer agent response format"""
from pydantic import BaseModel, Field

class ReportData(BaseModel):
    """class to format writer agent report data"""
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")