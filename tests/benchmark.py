from tools.registry import ToolRegistry
from tools.yahoo_tool import YahooFinanceTool
from tools.tavily_tool import TavilyTool
from tools.sec_tool import SECTool
from tools.scraper_tool import ScraperTool
from agents.research_agent import ResearchAgent


def build_agent():
    registry = ToolRegistry()
    registry.register(YahooFinanceTool())
    registry.register(TavilyTool())
    registry.register(SECTool())
    registry.register(ScraperTool())

    return ResearchAgent(registry)


def run_benchmarks():
    agent = build_agent()

    challenges = [
        "Analyze Apple stock using latest SEC filing and latest news.",
        "Analyze Microsoft as a long-term investment.",
        "Analyze NVIDIA and its AI growth opportunity.",
        "Analyze Tesla stock with risks and valuation.",
        "Analyze Amazon using latest news and financial data.",
        "Compare Apple and Microsoft as long-term investments.",
        "Analyze whether NVIDIA is overvalued.",
        "Create a professional investment research report on Meta.",
    ]

    results = []

    for index, query in enumerate(challenges, start=1):
        print(f"\nRunning Challenge {index}: {query}")

        try:
            report = agent.chat(query)

            results.append({
                "challenge": index,
                "query": query,
                "status": "PASS",
                "report_length": len(report),
            })

            print(f"Challenge {index}: PASS")

        except Exception as e:
            results.append({
                "challenge": index,
                "query": query,
                "status": "FAIL",
                "error": str(e),
            })

            print(f"Challenge {index}: FAIL - {e}")

    print("\nBenchmark Results:")
    for result in results:
        print(result)


if __name__ == "__main__":
    run_benchmarks()