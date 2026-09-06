"""integration test for pushover package"""
import os
from unittest import TestCase
from dotenv import load_dotenv
from notification_pusher.pushover import (
    PushOverConfig,
    PushOverClient
)

load_dotenv(override=True)

class IntegrationTestPushover(TestCase):
    """integration test suite for pushover"""

    def setUp(self) -> None:
        self.config = PushOverConfig(
            token = str(os.getenv("PUSHOVER_TOKEN")),
            user = str(os.getenv("PUSHOVER_USER")),
            url = str(os.getenv("PUSHOVER_URL"))
        )

        self.pushover = PushOverClient(config=self.config)

    def test_push_message(self) -> None:
        """test method push message"""
        self.pushover.push_message(
            message = "test-message",
            title = "test-title",
            priority = 1
        )