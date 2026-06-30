from app.llm import get_llm


class Planner:
    """
    Creates a research plan by deciding which tools are required.
    """

    def __init__(self):
        self.llm = get_llm()

    def create_plan(self, query: str) -> str:
        prompt = f"""
You are an autonomous financial research planner.

Available tools:

1. yahoo_finance
- stock price
- market cap
- pe ratio
- revenue

2. tavily
- latest news
- web search
- company announcements

3. scraper
- scrape article text from URLs returned by Tavily
- use only when tavily is also selected

4. sec
- SEC filings
- latest 10-K / 10-Q metadata
- annual reports
- official company filings

5. company_profile
- company overview
- CEO
- employees
- headquarters
- business summary

6. financial_calculator
- profit margin
- price-to-sales
- valuation classification
- requires yahoo_finance first

7. technical_indicator
- SMA 20
- SMA 50
- bullish or bearish trend
8. stock_comparison
- compare two companies
- use for Apple vs Microsoft, Nvidia vs AMD, Tesla vs BYD

9. currency_converter
- convert USD to other currencies

10. earnings_calendar
- upcoming earnings date
- earnings schedule

User Question:
{query}

Return ONLY valid JSON.

Example:
{{
    "tools": [
        "company_profile",
        "yahoo_finance",
        "financial_calculator",
        "technical_indicator",
        "stock_comparison",
        "tavily",
        "scraper",
        "sec",
        "currency_converter",
        "earnings_calendar"
    ]
}}

Rules:
- Do not write markdown.
- Do not write ```json.
- For stock analysis, include company_profile, yahoo_finance, and financial_calculator.
- For technical analysis, include technical_indicator.
- For stock comparison, include stock_comparison.
- For currency conversion, include currency_converter.
- If the query asks for news, include tavily and scraper.
- If the query asks for SEC filing, annual report, 10-K, or official filing, include sec.
"""

        response = self.llm.invoke(prompt)

        content = response.content.strip()
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        return content