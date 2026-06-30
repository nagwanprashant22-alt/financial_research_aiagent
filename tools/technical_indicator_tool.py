import yfinance as yf

from tools.base_tool import BaseTool


class TechnicalIndicatorTool(BaseTool):
    """
    Calculates basic technical indicators from price history.
    """

    def __init__(self):
        super().__init__(
            name="technical_indicator",
            description="Calculate moving averages and price trend signals.",
        )

    def execute(self, ticker: str):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="6mo")

            if hist.empty:
                return {
                    "success": False,
                    "tool": self.name,
                    "data": None,
                    "error": "No historical price data found.",
                    "fallback_used": False,
                }

            hist["SMA_20"] = hist["Close"].rolling(window=20).mean()
            hist["SMA_50"] = hist["Close"].rolling(window=50).mean()

            latest_close = round(float(hist["Close"].iloc[-1]), 2)
            sma_20 = round(float(hist["SMA_20"].iloc[-1]), 2)
            sma_50 = round(float(hist["SMA_50"].iloc[-1]), 2)

            trend = "Bullish" if sma_20 > sma_50 else "Bearish"

            return {
                "success": True,
                "tool": self.name,
                "data": {
                    "latest_close": latest_close,
                    "sma_20": sma_20,
                    "sma_50": sma_50,
                    "trend_signal": trend,
                },
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