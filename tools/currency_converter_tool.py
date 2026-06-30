import yfinance as yf

from tools.base_tool import BaseTool


class CurrencyConverterTool(BaseTool):
    """
    Convert USD to major currencies using Yahoo Finance.
    """

    def __init__(self):
        super().__init__(
            name="currency_converter",
            description="Convert USD into other currencies."
        )

    def execute(self, amount: float = 1.0, target_currency: str = "INR"):

        try:

            symbol = f"USD{target_currency}=X"

            ticker = yf.Ticker(symbol)

            rate = ticker.history(period="1d")["Close"].iloc[-1]

            converted = round(amount * float(rate), 2)

            return {
                "success": True,
                "tool": self.name,
                "data": {
                    "amount_usd": amount,
                    "target_currency": target_currency,
                    "exchange_rate": round(float(rate), 4),
                    "converted_amount": converted,
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