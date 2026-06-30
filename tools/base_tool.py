from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Abstract base class for all tools.
    Every tool in the project will inherit from this class.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the tool.
        """
        pass