import json
from datetime import datetime
from pathlib import Path


class EpisodicMemory:
    """
    Stores each research run as an event log.
    """

    def __init__(self, log_file: str = "data/episodic_memory.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def save_event(self, query: str, plan: dict, tool_results: dict):
        event = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "plan": plan,
            "tool_results": tool_results,
        }

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")