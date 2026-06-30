from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.nodes import planner_node, tool_node


class AgentState(TypedDict):
    query: str
    plan: dict
    ticker: str
    tool_results: dict
    final_report: str


workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("planner")

workflow.add_edge("planner", "tools")
workflow.add_edge("tools", END)

graph = workflow.compile()