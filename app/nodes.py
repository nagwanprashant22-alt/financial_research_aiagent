import json

from app.llm import get_llm

llm = get_llm()


def planner_node(state):
    from tools.yahoo_tool import YahooFinanceTool
from tools.tavily_tool import TavilyTool


yahoo = YahooFinanceTool()
tavily = TavilyTool()


def extract_ticker(query: str):

    prompt = f"""
Extract ONLY the stock ticker.

Question:
{query}

Return ONLY the ticker.

Examples:

Apple -> AAPL
Tesla -> TSLA
Microsoft -> MSFT
NVIDIA -> NVDA
"""

    response = llm.invoke(prompt)

    return response.content.strip().upper()


def tool_node(state):

    results = {}

    tools = state["plan"].get("tools", [])

    if "yahoo_finance" in tools:

        ticker = extract_ticker(state["query"])

        state["ticker"] = ticker

        results["yahoo_finance"] = yahoo.execute(
            ticker=ticker
        )

    if "tavily" in tools:

        results["tavily"] = tavily.execute(
            query=state["query"]
        )

    state["tool_results"] = results

    return state

    prompt = f"""
You are an autonomous Financial Research Planner.

Available tools:

1. yahoo_finance
2. tavily

User Question:

{state["query"]}

Return ONLY JSON.

Example:

{{
    "tools":[
        "yahoo_finance",
        "tavily"
    ]
}}
"""

    response = llm.invoke(prompt)

    content = (
        response.content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        state["plan"] = json.loads(content)
    except Exception:
        state["plan"] = {
            "tools": ["yahoo_finance"]
        }

    return state