"""script for notification pusher"""
import requests
from .pushover_config import PushOverConfig

class PushOverClient:
    """class for notification pusher"""
    def __init__(self, config: PushOverConfig) -> None:
        """class initialization"""
        self.config = config

    def push_message(self,
                     message: str,
                     title: str | None = None,
                     priority: int | None = None) -> dict[str, int]:
        """method to post notification
        Args:
            message (str): notification message
            title (str | None): notification title
            priority (int | None): notification priority
        Raises:
            ValueError: if notification message is empty string
        """
        if not message.strip():
            raise ValueError("notification message cannot be empty")

        notification_data: dict[str, str | int] = {
            "token": self.config.token,
            "user": self.config.user,
            "message": message
        }

        if title is not None:
            notification_data['title'] = title

        if priority is not None:
            notification_data['priority'] = priority
        
        response = requests.post(
            self.config.url,
            data = notification_data,
            timeout=10,
        )

        return {"status": response.status_code}