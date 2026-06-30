from utils.ticker import get_two_tickers
class Executor:
    
    """
    Executes all tools requested by the planner with safe error handling.
    """

    def __init__(self, registry):
        self.registry = registry

    def execute_plan(self, plan: dict, query: str, ticker: str | None = None):
        results = {}

        for tool_name in plan.get("tools", []):
            tool = self.registry.get(tool_name)

            if tool is None:
                results[tool_name] = {
                    "success": False,
                    "tool": tool_name,
                    "data": None,
                    "error": f"{tool_name} not registered.",
                    "fallback_used": False,
                }
                continue

            try:
                if tool_name == "stock_comparison":
                    from utils.ticker import get_two_tickers
                    ticker1, ticker2 = get_two_tickers(query)
                    result = tool.execute(ticker1, ticker2)

                elif tool_name == "yahoo_finance":
                    result = tool.execute(ticker=ticker)

                elif tool_name == "company_profile":
                    result = tool.execute(ticker=ticker)

                elif tool_name == "technical_indicator":
                    result = tool.execute(ticker=ticker)

                elif tool_name == "financial_calculator":
                    yahoo_result = results.get("yahoo_finance", {})
                    yahoo_data = yahoo_result.get("data")
                    result = tool.execute(financial_data=yahoo_data) if yahoo_data else {
                        "success": False, "tool": tool_name, "data": None,
                        "error": "Yahoo Finance data required.", "fallback_used": False
                    }

                elif tool_name == "tavily":
                    result = tool.execute(query=query)

                elif tool_name == "sec":
                    result = tool.execute(ticker=ticker)

                elif tool_name == "scraper":
                    tavily_data = (results.get("tavily", {}).get("data")) or []
                    if tavily_data and isinstance(tavily_data, list):
                        result = tool.execute(url=tavily_data[0].get("url"))
                    else:
                        result = {
                            "success": False, "tool": tool_name, "data": None,
                            "error": "No Tavily URL available.", "fallback_used": False
                        }
                elif tool_name == "currency_converter":
                      result = tool.execute(amount=100, target_currency="INR")

                elif tool_name == "earnings_calendar":
                    result = tool.execute(ticker=ticker)              

                else:
                    result = {
                        "success": False, "tool": tool_name, "data": None,
                        "error": "Unsupported tool.", "fallback_used": False
                    }

                results[tool_name] = result

            except Exception as e:
                results[tool_name] = {
                    "success": False, "tool": tool_name, "data": None,
                    "error": str(e), "fallback_used": False
                }

        return results