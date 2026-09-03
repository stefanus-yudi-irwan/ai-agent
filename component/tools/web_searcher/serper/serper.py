"""class to connect to serper websearch tool"""
import requests
from component.tools.web_searcher.serper.serper_config import SerperWebSearchConfig

class SerperWebSearch:
    """web search tool using serper"""
    def __init__(self, 
                 config: SerperWebSearchConfig) -> None:
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

        except Exception as e:
            return f"Error executing search: {str(e)}"
