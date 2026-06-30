from typing import Dict

from tools.base_tool import BaseTool


class ToolRegistry:
    """
    Stores and manages all available tools.
    """

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        """
        Register a new tool.
        """
        self.tools[tool.name] = tool

    def get(self, tool_name: str):
        """
        Retrieve a tool by name.
        """
        return self.tools.get(tool_name)

    def list_tools(self):
        """
        Return all registered tool names.
        """
        return list(self.tools.keys())