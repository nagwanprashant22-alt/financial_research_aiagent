from tools.base_tool import BaseTool


class DummyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="dummy",
            description="A simple testing tool"
        )

    def execute(self):
        return "Dummy Tool Executed Successfully!"