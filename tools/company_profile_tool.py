import yfinance as yf

from tools.base_tool import BaseTool


class CompanyProfileTool(BaseTool):
    """
    Fetch detailed company profile using Yahoo Finance.
    """

    def __init__(self):
        super().__init__(
            name="company_profile",
            description="Fetch company profile information."
        )

    def execute(self, ticker: str):

        try:

            stock = yf.Ticker(ticker)

            info = stock.info

            data = {
                "company": info.get("longName"),
                "symbol": ticker.upper(),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "city": info.get("city"),
                "website": info.get("website"),
                "employees": info.get("fullTimeEmployees"),
                "exchange": info.get("exchange"),
                "currency": info.get("currency"),
                "ceo": info.get("companyOfficers", [{}])[0].get("name"),
                "summary": info.get("longBusinessSummary"),
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