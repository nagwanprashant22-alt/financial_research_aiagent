import requests

from tools.base_tool import BaseTool


class SECTool(BaseTool):
    """
    Fetch latest SEC filings using SEC's official submissions API.
    """

    def __init__(self):
        super().__init__(
            name="sec",
            description="Fetch latest SEC filings."
        )

        self.headers = {
            "User-Agent": "FinancialResearchAgent/1.0 nagwanprashant22@gmail.com"
        }

    def execute(self, ticker: str):

        try:

            # Step 1: Find CIK from ticker
            ticker_url = "https://www.sec.gov/files/company_tickers.json"

            response = requests.get(
                ticker_url,
                headers=self.headers,
                timeout=20
            )

            response.raise_for_status()

            companies = response.json()

            cik = None

            for company in companies.values():

                if company["ticker"].upper() == ticker.upper():

                    cik = str(company["cik_str"]).zfill(10)

                    break

            if cik is None:

                return {
                    "success": False,
                    "tool": self.name,
                    "data": None,
                    "error": f"Ticker '{ticker}' not found."
                }

            # Step 2: Fetch company submissions
            filing_url = (
                f"https://data.sec.gov/submissions/CIK{cik}.json"
            )

            filing_response = requests.get(
                filing_url,
                headers=self.headers,
                timeout=20
            )

            filing_response.raise_for_status()

            filings = filing_response.json()

            recent = filings["filings"]["recent"]

            data = {
                "company": filings["name"],
                "ticker": ticker.upper(),
                "latest_form": recent["form"][0],
                "filing_date": recent["filingDate"][0],
                "accession_number": recent["accessionNumber"][0],
            }

            return {
                "success": True,
                "tool": self.name,
                "data": data,
                "error": None
            }

        except Exception as e:

            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": str(e)
            }