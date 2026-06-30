import yfinance as yf

from tools.base_tool import BaseTool


class StockComparisonTool(BaseTool):
    """
    Compare two stocks using Yahoo Finance.
    """

    def __init__(self):
        super().__init__(
            name="stock_comparison",
            description="Compare two companies using key financial metrics.",
        )

    def execute(self, ticker1: str, ticker2: str):

        try:

            stock1 = yf.Ticker(ticker1)
            stock2 = yf.Ticker(ticker2)

            info1 = stock1.info
            info2 = stock2.info

            data = {
                ticker1.upper(): {
                    "company": info1.get("longName"),
                    "market_cap": info1.get("marketCap"),
                    "current_price": info1.get("currentPrice"),
                    "pe_ratio": info1.get("trailingPE"),
                    "revenue": info1.get("totalRevenue"),
                },
                ticker2.upper(): {
                    "company": info2.get("longName"),
                    "market_cap": info2.get("marketCap"),
                    "current_price": info2.get("currentPrice"),
                    "pe_ratio": info2.get("trailingPE"),
                    "revenue": info2.get("totalRevenue"),
                },
            }

            return {
                "success": True,
                "tool": self.name,
                "data": data,
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