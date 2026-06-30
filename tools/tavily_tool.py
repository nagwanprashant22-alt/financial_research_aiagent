from tavily import TavilyClient

from configs.settings import settings
from tools.base_tool import BaseTool


class TavilyTool(BaseTool):
    """
    Search the web using Tavily.
    """

    def __init__(self):
        super().__init__(
            name="tavily",
            description="Search the web for financial information.",
        )

        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def execute(self, query: str):

        try:

            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
            )

            return {
                "success": True,
                "tool": self.name,
                "data": response["results"],
                "error": None,
            }

        except Exception as e:

            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": str(e),
            }