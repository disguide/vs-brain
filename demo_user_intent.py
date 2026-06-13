from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.assistant_agent import AssistantAgent
from src.agents.user_intent_agent import UserIntentDiscoveryAgent
from src.agents.info_gathering_agent import InfoGatheringAgent
from src.harness.orchestration_manager import OrchestrationManager

def main():
    # 1. Initialize agents
    orchestrator = OrchestratorAgent(name="MasterMind", model_name="gpt-4-turbo")
    assistant = AssistantAgent(name="CoPilot", model_name="gpt-4-turbo")
    user_intent_agent = UserIntentDiscoveryAgent(name="Clarifier", model_name="gpt-4-turbo")
    info_agent = InfoGatheringAgent(name="InfoSeeker", model_name="gpt-4-turbo")

    # 2. Setup Orchestration Manager
    manager = OrchestrationManager(orchestrator, assistant)
    manager.register_user_intent_agent(user_intent_agent)
    manager.register_specialized_agent("InfoGatheringAgent", info_agent)

    # 3. Demonstrate with vague input
    print("--- Case 1: Vague User Input ---")
    vague_input = "I want info."
    manager.run_orchestration(vague_input)

    # 4. Demonstrate with clear input
    print("\n--- Case 2: Clear User Input ---")
    clear_input = "Research the latest advancements in autonomous AI agents for 2026."
    manager.run_orchestration(clear_input)

if __name__ == "__main__":
    main()
