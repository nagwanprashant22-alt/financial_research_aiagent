from tools.base_tool import BaseTool


class FinancialCalculatorTool(BaseTool):
    """
    Calculates additional financial metrics from Yahoo Finance data.
    """

    def __init__(self):
        super().__init__(
            name="financial_calculator",
            description="Calculate additional financial ratios."
        )

    def execute(self, financial_data: dict):

        try:
            current_price = financial_data.get("current_price")
            market_cap = financial_data.get("market_cap")
            revenue = financial_data.get("revenue")
            net_income = financial_data.get("net_income")

            profit_margin = None
            if revenue and net_income:
                profit_margin = round((net_income / revenue) * 100, 2)

            price_to_sales = None
            if revenue and market_cap:
                price_to_sales = round(market_cap / revenue, 2)

            valuation = "Unknown"

            pe = financial_data.get("pe_ratio")

            if pe:
                if pe < 15:
                    valuation = "Undervalued"
                elif pe < 30:
                    valuation = "Fairly Valued"
                else:
                    valuation = "Potentially Overvalued"

            return {
                "success": True,
                "tool": self.name,
                "data": {
                    "profit_margin_percent": profit_margin,
                    "price_to_sales": price_to_sales,
                    "valuation": valuation,
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