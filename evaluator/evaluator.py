class Evaluator:
    """
    Evaluates generated research reports across quality metrics.
    """

    def evaluate(self, report: str, tool_results: dict):
        metrics = {
            "has_executive_summary": "Executive Summary" in report,
            "has_company_overview": "Company Overview" in report,
            "has_financial_analysis": "Financial Analysis" in report,
            "has_latest_news": "Latest News" in report or "News" in report,
            "has_risks": "Risks" in report,
            "has_recommendation": "Recommendation" in report,
            "has_disclaimer": "Disclaimer" in report,
            "uses_yahoo_finance": "yahoo_finance" in tool_results,
            "uses_tavily": "tavily" in tool_results,
            "uses_sec": "sec" in tool_results,
            "uses_scraper": "scraper" in tool_results,
            "tool_count": len(tool_results),
            "successful_tools": sum(
                1 for r in tool_results.values()
                if isinstance(r, dict) and r.get("success")
            ),
            "failed_tools": sum(
                1 for r in tool_results.values()
                if isinstance(r, dict) and not r.get("success")
            ),
            "report_length": len(report),
            "has_multi_source_synthesis": "synthesis" in report.lower(),
            "has_conflict_discussion": "conflict" in report.lower() or "mixed" in report.lower(),
            "has_valuation_discussion": "valuation" in report.lower(),
            "has_sec_discussion": "sec" in report.lower() or "filing" in report.lower(),
            "has_source_reliability": "reliability" in report.lower() or "source" in report.lower(),
            "quality_score": 0,
        }

        boolean_metrics = [
            value for value in metrics.values()
            if isinstance(value, bool)
        ]

        metrics["quality_score"] = round(
            sum(boolean_metrics) / len(boolean_metrics) * 100,
            2
        )

        return metrics