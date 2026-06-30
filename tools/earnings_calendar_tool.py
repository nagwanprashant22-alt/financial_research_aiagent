import yfinance as yf

from tools.base_tool import BaseTool


class EarningsCalendarTool(BaseTool):
    """
    Fetch upcoming earnings information.
    """

    def __init__(self):
        super().__init__(
            name="earnings_calendar",
            description="Fetch upcoming earnings dates."
        )

    def execute(self, ticker: str):

        try:

            stock = yf.Ticker(ticker)

            calendar = stock.calendar

            return {
                "success": True,
                "tool": self.name,
                "data": str(calendar),
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