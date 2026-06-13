from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.assistant_agent import AssistantAgent
from src.agents.user_intent_agent import UserIntentDiscoveryAgent
from src.agents.info_gathering_agent import InfoGatheringAgent
from src.agents.verification_agent import VerificationAgent
from src.agents.obsidian_agent import ObsidianAgent
from src.harness.orchestration_manager import OrchestrationManager

def main():
    # 1. Initialize core agents
    orchestrator = OrchestratorAgent(name="Strategist", model_name="gpt-4-turbo")
    assistant = AssistantAgent(name="Coordinator", model_name="gpt-4-turbo")
    user_intent_agent = UserIntentDiscoveryAgent(name="Discovery", model_name="gpt-4-turbo")

    # 2. Initialize specialized agents with Second Brain capabilities
    info_agent = InfoGatheringAgent(name="Researcher", model_name="gpt-4-turbo")
    verifier = VerificationAgent(name="Verifier", model_name="gpt-4-turbo")
    obsidian_agent = ObsidianAgent(name="Librarian", model_name="gpt-4-turbo", vault_path="/home/ubuntu/obsidian_vault")

    # 3. Setup Orchestration Manager with Agent-MCP Knowledge Graph
    manager = OrchestrationManager(orchestrator, assistant)
    manager.register_user_intent_agent(user_intent_agent)
    manager.register_specialized_agent("InfoGatheringAgent", info_agent)
    manager.register_specialized_agent("VerificationAgent", verifier)
    manager.register_specialized_agent("ObsidianAgent", obsidian_agent)

    # 4. Define a complex task for the LLM Wiki
    task = "Develop a comprehensive knowledge base on the current state of AI Agents in 2026."

    print("--- Starting Full-Stack AI Second Brain Orchestration ---")
    
    # 5. Run the orchestration
    # This will follow: Discovery -> Planning (CrewAI) -> Execution (Info Gathering) -> 
    # Verification -> Knowledge Management (PARA + Obsidian Skills) -> Shared Memory (Agent-MCP)
    manager.run_orchestration(task, require_verification=True)

    # 6. Demonstrate QMD Retrieval
    print("\n--- Demonstrating QMD-style Retrieval from LLM Wiki ---")
    retrieval_query = "latest agent orchestration patterns"
    context = obsidian_agent.retrieve(retrieval_query)
    print(f"Retrieved Context: {context}")

if __name__ == "__main__":
    main()
