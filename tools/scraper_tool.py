import requests
from bs4 import BeautifulSoup

from tools.base_tool import BaseTool


class ScraperTool(BaseTool):
    """
    Scrapes readable text from a webpage URL.
    """

    def __init__(self):
        super().__init__(
            name="scraper",
            description="Scrape readable text from a webpage URL.",
        )

    def execute(self, url: str):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 FinancialResearchAgent/1.0"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

            return {
                "success": True,
                "tool": self.name,
                "data": text[:5000],
                "error": None,
                "fallback_used": False,
            }

        except Exception as e:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": str(e),
                "fallback_used": False,
            }