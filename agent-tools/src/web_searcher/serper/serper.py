"""class to connect to serper websearch tool"""
import requests
from loguru import logger
from .serper_config import SerperWebSearchConfig

class SerperWebSearchError(Exception):
    """Raise when a Serper web search fails."""

class SerperWebSearch:
    """web search tool using serper"""
    def __init__(self, config: SerperWebSearchConfig) -> None:
        self.config = config
        self.headers = {
            'X-API-KEY': self.config.api_key,
            'Content-Type': 'application/json'
        }
        self.payload = {
            "gl": self.config.geographic_preference,
            "hl": self.config.language_preference
        }

    def search_in_web(self, message: str) -> str:
        """Queries the Serper.dev Google Search API to fetch live search results.
        Args:
            message (str): string to be searched
        Returns:
            str: _description_
        """
        self.payload['q'] = message

        try:
            response = requests.post(self.config.url,
                                     headers=self.headers,
                                     json=self.payload, 
                                     timeout=10000)
            response.raise_for_status()
            results = response.json()

            snippets = [
                item.get("snippet", "")
                for item in results.get("organic", [])
                if "snippet" in item
            ]

            return "\n\n".join(snippets) if snippets else "No results found."

        except requests.exceptions.Timeout as e:
            error = SerperWebSearchError("request to serper API timed out")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e

        except requests.exceptions.ConnectionError as e:
            error = SerperWebSearchError("could not connect to serper API")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e

        except requests.exceptions.HTTPError as e:
            error = SerperWebSearchError(f"serper API returned HTTP {e.response.status_code}")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e

        except requests.exceptions.JSONDecodeError as e:
            error = SerperWebSearchError("serper API returned an invalid JSON response")
            logger.error(f"{type(error).__name__}: {error}")
            raise error from e