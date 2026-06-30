import yfinance as yf

from tools.base_tool import BaseTool


class YahooFinanceTool(BaseTool):
    """
    Fetch financial information using Yahoo Finance.
    """

    def __init__(self):
        super().__init__(
            name="yahoo_finance",
            description="Fetch stock information from Yahoo Finance",
        )

    def execute(self, ticker: str):

        try:
            ticker = ticker.upper()

            stock = yf.Ticker(ticker)
            info = stock.info

            data = {
                "company": info.get("longName"),
                "symbol": ticker,
                "current_price": info.get("currentPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "dividend_yield": info.get("dividendYield"),
                "revenue": info.get("totalRevenue"),
                "net_income": info.get("netIncomeToCommon"),
            }

            return {
                "success": True,
                "tool": self.name,
                "data": data,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": str(e),
            }