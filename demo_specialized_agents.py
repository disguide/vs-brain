from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.assistant_agent import AssistantAgent
from src.agents.info_gathering_agent import InfoGatheringAgent
from src.agents.verification_agent import VerificationAgent
from src.agents.obsidian_agent import ObsidianAgent
from src.harness.orchestration_manager import OrchestrationManager

def main():
    # 1. Initialize the core agents
    orchestrator = OrchestratorAgent(name="MasterMind", model_name="gpt-4-turbo")
    assistant = AssistantAgent(name="CoPilot", model_name="gpt-4-turbo")

    # 2. Initialize specialized agents
    info_agent = InfoGatheringAgent(name="InfoSeeker", model_name="gpt-4-turbo")
    verifier = VerificationAgent(name="TruthChecker", model_name="gpt-4-turbo")
    obsidian_agent = ObsidianAgent(name="KnowledgeLibrarian", model_name="gpt-4-turbo", vault_path="/home/ubuntu/obsidian_vault")

    # 3. Setup the Orchestration Manager
    manager = OrchestrationManager(orchestrator, assistant)
    manager.register_specialized_agent("InfoGatheringAgent", info_agent)
    manager.register_specialized_agent("VerificationAgent", verifier)
    manager.register_specialized_agent("ObsidianAgent", obsidian_agent)

    # 4. Define a task that will trigger conditional verification
    task = "Research current trends in artificial general intelligence."

    # 5. Run the orchestration with conditional verification and Obsidian integration
    print("--- Demonstrating Specialized Agents (Verification & Obsidian) ---")
    manager.run_orchestration(task, require_verification=True)

if __name__ == "__main__":
    main()
