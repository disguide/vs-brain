from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.assistant_agent import AssistantAgent
from src.agents.info_gathering_agent import InfoGatheringAgent
from src.harness.orchestration_manager import OrchestrationManager

def main():
    # 1. Initialize the Orchestrator and Assistant
    orchestrator = OrchestratorAgent(name="MasterMind", model_name="gpt-4-turbo")
    assistant = AssistantAgent(name="CoPilot", model_name="gpt-4-turbo")

    # 2. Initialize specialized agents
    info_agent = InfoGatheringAgent(name="InfoSeeker", model_name="gpt-4-turbo")

    # 3. Setup the Orchestration Manager
    manager = OrchestrationManager(orchestrator, assistant)
    manager.register_specialized_agent("InfoGatheringAgent", info_agent)

    # 4. Define a complex task
    complex_task = "Research the latest advancements in quantum computing and provide a summary report."

    # 5. Run the orchestration
    manager.run_orchestration(complex_task)

if __name__ == "__main__":
    main()
