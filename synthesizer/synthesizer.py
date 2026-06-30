class Synthesizer:
    """
    Pure Python synthesis engine.
    Combines tool outputs and highlights evidence quality.
    """

    def synthesize(self, query: str, tool_results: dict, react_steps: list) -> str:
        confirmed_facts = []
        conflicts = []
        reliability = []

        if "sec" in tool_results and tool_results["sec"]:
            sec_result = tool_results["sec"]
            reliability.append("SEC filings: High reliability")
            if sec_result.get("success"):
                confirmed_facts.append(
                    f"SEC data available: {sec_result.get('data')}"
                )
            else:
                conflicts.append(
                    f"SEC unavailable: {sec_result.get('error')}"
                )

        if "yahoo_finance" in tool_results and tool_results["yahoo_finance"]:
            yahoo_result = tool_results["yahoo_finance"]
            reliability.append("Yahoo Finance: Medium-High reliability")
            if yahoo_result.get("success"):
                confirmed_facts.append(
                    f"Financial market data available: {yahoo_result.get('data')}"
                )
            else:
                conflicts.append(
                    f"Yahoo Finance unavailable: {yahoo_result.get('error')}"
                )

        if "tavily" in tool_results and tool_results["tavily"]:
            tavily_result = tool_results["tavily"]
            reliability.append("Web/news search: Medium reliability")
            if tavily_result.get("success"):
                confirmed_facts.append(
                    "Recent web/news evidence was collected."
                )
            else:
                conflicts.append(
                    f"Tavily unavailable: {tavily_result.get('error')}"
                )

        if "scraper" in tool_results and tool_results["scraper"]:
            scraper_result = tool_results["scraper"]
            reliability.append("Scraped article text: Medium reliability")
            if scraper_result.get("success"):
                confirmed_facts.append(
                    "Detailed article text was scraped from a web source."
                )
            else:
                conflicts.append(
                    f"Scraper unavailable: {scraper_result.get('error')}"
                )

        if not confirmed_facts:
            confirmed_facts.append(
                "No strong external evidence was collected. Report should be cautious."
            )

        if not conflicts:
            conflicts.append(
                "No major tool conflicts detected. Differences may still exist across sources."
            )

        return {
            "query": query,
            "confirmed_facts": confirmed_facts,
            "conflicting_or_missing_evidence": conflicts,
            "source_reliability": reliability,
            "react_steps_count": len(react_steps),
            "interpretation": (
                "Prioritize SEC data for official filings, Yahoo Finance for market metrics, "
                "and Tavily/scraped sources for recent news context."
            ),
        }