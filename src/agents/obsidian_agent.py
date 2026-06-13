from src.agents.base_agent import BaseAgent
from typing import List, Dict, Any

class ObsidianAgent(BaseAgent):
    """
    A specialized agent for knowledge management and integration with Obsidian.
    """

    def __init__(self, name: str, model_name: str, vault_path: str):
        super().__init__(name, model_name)
        self.vault_path = vault_path

    def act(self, info_to_save: Any) -> str:
        """
        Organizes and saves information into the Obsidian vault using PARA structure.
        """
        if isinstance(info_to_save, str):
            title = "New Note"
            content = info_to_save
            category = "Resources"
        else:
            title = info_to_save.get("title", "New Note")
            content = info_to_save.get("content", "")
            category = info_to_save.get("category", "Resources") 
        
        print(f"{self.name} (Obsidian) is saving note: {title} to {self.vault_path}/{category}")
        # In a real implementation, this would involve using obsidian_save_note with the category folder
        return f"Successfully saved information to Obsidian note: [{category}] {title}"

    def retrieve(self, query: str) -> str:
        """
        Retrieves information from the vault using QMD-inspired hybrid search.
        """
        print(f"{self.name} (Obsidian) is performing QMD-style hybrid search for: {query}")
        # Simulating QMD's BM25 + Vector retrieval
        return f"QMD Retrieval Result: Found relevant context for '{query}' in the PARA vault."

    def plan(self, info: Dict[str, str]) -> List[str]:
        """
        Plans the organization and storage of information in Obsidian.
        """
        return [
            "Classify content into PARA categories (Projects, Areas, Resources, Archive)",
            "Format content with standardized frontmatter (Obsidian Skills)",
            "Create or update note in the categorized folder",
            "Establish links and backlinks for Graphify visualization"
        ]
