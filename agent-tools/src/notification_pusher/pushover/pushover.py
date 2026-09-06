"""script for notification pusher"""
import requests
from loguru import logger
from .pushover_config import PushOverConfig

class PushOverClientError(Exception):
    """Raise when pushover notification client get error"""

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
            error = ValueError("notification message cannot be empty")
            logger.error(f"{type(error).__name__}: ")
            raise error

        notification_data: dict[str, str | int] = {
            "token": self.config.token,
            "user": self.config.user,
            "message": message
        }

        if title is not None:
            notification_data['title'] = title

        if priority is not None:
            notification_data['priority'] = priority

        try:
            response = requests.post(
                self.config.url,
                data = notification_data,
                timeout=10,
            )
            response.raise_for_status()
            results = response.json()
            return results

        except requests.exceptions.HTTPError as e:
            error = PushOverClientError(f"pushover API returned HTTP {e.response.status_code}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e
        