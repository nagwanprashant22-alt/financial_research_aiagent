import json

from app.llm import get_llm
from agents.executor import Executor
from agents.planner import Planner
from evaluator.evaluator import Evaluator
from memory.episodic import EpisodicMemory
from memory.long_term import LongTermMemory
from memory.short_term import ShortTermMemory
from synthesizer.synthesizer import Synthesizer
from utils.ticker import get_ticker


class ResearchAgent:
    def __init__(self, registry):
        self.llm = get_llm()
        self.registry = registry
        self.executor = Executor(registry)
        self.planner = Planner()

        self.memory = ShortTermMemory()
        self.episodic_memory = EpisodicMemory()
        self.long_term_memory = LongTermMemory()

        self.synthesizer = Synthesizer()
        self.evaluator = Evaluator()

    def run(self, query: str) -> dict:
        self.memory.add("user", query)

        previous_research = self.long_term_memory.search(query)

        plan_text = self.planner.create_plan(query)

        try:
            plan = json.loads(plan_text)
        except Exception:
            plan = {
                "tools": [
                    "company_profile",
                    "yahoo_finance",
                    "financial_calculator",
                    "technical_indicator",
                    "tavily",
                    "scraper",
                    "sec",
                ]
            }

        ticker = get_ticker(query)

        react_steps = []
        tool_results = {}

        for tool_name in plan.get("tools", []):
            react_step = {
                "thought": f"Using {tool_name} to gather evidence.",
                "action": tool_name,
            }

            observation = self.executor.execute_plan(
                plan={"tools": [tool_name]},
                query=query,
                ticker=ticker,
            )

            react_step["observation"] = observation
            react_steps.append(react_step)
            tool_results[tool_name] = observation.get(tool_name)

        synthesis = self.synthesizer.synthesize(
            query=query,
            tool_results=tool_results,
            react_steps=react_steps,
        )

        prompt = f"""
You are a Senior Equity Research Analyst.

User Question:
{query}

Ticker:
{ticker}

Previous Research:
{json.dumps(previous_research, indent=2, default=str)}

Research Plan:
{json.dumps(plan, indent=2)}

Tool Results:
{json.dumps(tool_results, indent=2, default=str)}

Evidence Synthesis:
{json.dumps(synthesis, indent=2, default=str)}

Write a professional investment research report.

Include:

1. Executive Summary
2. Company Overview
3. Financial Analysis
4. Latest News
5. SEC Filing Insights
6. Multi-Source Synthesis
7. Risks
8. Investment Recommendation
9. Disclaimer
"""

        response = self.llm.invoke(prompt)
        report = response.content

        evaluation = self.evaluator.evaluate(
            report=report,
            tool_results=tool_results,
        )

        self.memory.add("assistant", report)

        self.episodic_memory.save_event(
            query=query,
            plan=plan,
            tool_results=tool_results,
        )

        self.long_term_memory.add(
            query=query,
            report=report,
        )

        return {
            "query": query,
            "ticker": ticker,
            "plan": plan,
            "react_steps": react_steps,
            "tool_results": tool_results,
            "synthesis": synthesis,
            "report": report,
            "evaluation": evaluation,
            "previous_research": previous_research,
        }

    def chat(self, query: str) -> str:
        result = self.run(query)
        return result["report"]