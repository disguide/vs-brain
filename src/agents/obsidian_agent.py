from src.agents.base_agent import BaseAgent
from typing import List, Dict, Any

class ObsidianAgent(BaseAgent):
    """
    A specialized agent for knowledge management and integration with Obsidian.
    """

    def __init__(self, name: str, model_name: str, vault_path: str):
        super().__init__(name, model_name)
        self.vault_path = vault_path

    def act(self, info_to_save: Dict[str, str]) -> str:
        """
        Organizes and saves information into the Obsidian vault.
        """
        title = info_to_save.get("title", "New Note")
        content = info_to_save.get("content", "")
        print(f"{self.name} (Obsidian) is saving note: {title} to {self.vault_path}")
        # In a real implementation, this would involve using the obsidian tool to write to the vault
        return f"Successfully saved information to Obsidian note: {title}"

    def plan(self, info: Dict[str, str]) -> List[str]:
        """
        Plans the organization and storage of information in Obsidian.
        """
        return [
            "Determine appropriate folder and tags",
            "Format content for Obsidian (Markdown)",
            "Create or update note in the vault",
            "Establish links to related notes"
        ]
