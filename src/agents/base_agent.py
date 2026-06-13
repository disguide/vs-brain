from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in the vs-brain framework.
    """

    def __init__(self, name: str, model_name: str):
        self.name = name
        self.model_name = model_name
        self.memory: List[Dict[str, Any]] = []

    @abstractmethod
    def act(self, task: str) -> str:
        """
        Takes a task as input and returns the agent's response.
        """
        pass

    @abstractmethod
    def plan(self, task: str) -> List[str]:
        """
        Decomposes a task into a series of steps.
        """
        pass

    def add_to_memory(self, entry: Dict[str, Any]):
        """
        Adds an entry to the agent's memory.
        """
        self.memory.append(entry)

    def get_memory(self) -> List[Dict[str, Any]]:
        """
        Returns the agent's memory.
        """
        return self.memory
