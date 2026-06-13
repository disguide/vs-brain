from src.agents.base_agent import BaseAgent
from typing import List, Dict, Any

class AssistantAgent(BaseAgent):
    """
    The Orchestrator's primary deputy, managing inter-agent communication and state.
    """

    def __init__(self, name: str, model_name: str):
        super().__init__(name, model_name)
        self.shared_state: Dict[str, Any] = {}

    def act(self, task: str) -> str:
        """
        Manages the execution of a specific sub-task or communication.
        """
        print(f"{self.name} (Assistant) is managing sub-task: {task}")
        # In a real implementation, this would involve coordinating with specialized agents
        return f"Assistant has processed sub-task: {task}"

    def plan(self, task: str) -> List[str]:
        """
        Plans the coordination for a specific sub-task.
        """
        return [
            "Identify target specialized agent",
            "Prepare sub-task instructions",
            "Monitor execution",
            "Capture and record results"
        ]

    def update_state(self, key: str, value: Any):
        """
        Updates the shared workflow state.
        """
        self.shared_state[key] = value
        print(f"Assistant updated state: {key} = {value}")
