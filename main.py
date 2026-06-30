from configs.logger import logger
from tools.registry import ToolRegistry
from tools.yahoo_tool import YahooFinanceTool
from tools.tavily_tool import TavilyTool
from tools.sec_tool import SECTool
from tools.scraper_tool import ScraperTool
from tools.company_profile_tool import CompanyProfileTool
from tools.financial_calculator_tool import FinancialCalculatorTool
from agents.research_agent import ResearchAgent
from tools.technical_indicator_tool import TechnicalIndicatorTool
from tools.stock_comparison_tool import StockComparisonTool
from tools.currency_converter_tool import CurrencyConverterTool
from tools.earnings_calendar_tool import EarningsCalendarTool


def main():
    logger.info("Financial Research Agent Started")

    registry = ToolRegistry()

    registry.register(YahooFinanceTool())
    registry.register(TavilyTool())
    registry.register(SECTool())
    registry.register(ScraperTool())
    registry.register(CompanyProfileTool())
    registry.register(FinancialCalculatorTool())
    registry.register(TechnicalIndicatorTool())
    registry.register(StockComparisonTool())
    registry.register(CurrencyConverterTool())
    registry.register(EarningsCalendarTool())

    print("Registered Tools:")
    print(registry.list_tools())

    agent = ResearchAgent(registry)

    query = input("\nAsk your research question:\n> ")

    answer = agent.chat(query)

    print("\n")
    print("=" * 70)
    print(answer)
    print("=" * 70)


if __name__ == "__main__":
    main()