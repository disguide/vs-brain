from typing import List, Dict, Any
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.assistant_agent import AssistantAgent
from src.agents.base_agent import BaseAgent

class OrchestrationManager:
    """
    Manages the multi-agent orchestration workflow within the vs-brain harness.
    """

    def __init__(self, orchestrator: OrchestratorAgent, assistant: AssistantAgent):
        self.orchestrator = orchestrator
        self.assistant = assistant
        self.specialized_agents: Dict[str, BaseAgent] = {}

    def register_specialized_agent(self, agent_type: str, agent: BaseAgent):
        """
        Registers a specialized agent for use in orchestration.
        """
        self.specialized_agents[agent_type] = agent

    def run_orchestration(self, main_task: str, require_verification: bool = False):
        """
        Executes the full orchestration workflow for a complex task.
        """
        print(f"\n--- Starting Multi-Agent Orchestration for: {main_task} ---")
        
        # 1. Orchestrator analyzes and plans
        self.orchestrator.act(main_task)
        plan = self.orchestrator.plan_steps
        
        # 2. Iterate through the plan
        for step in plan:
            step_id = step["id"]
            sub_task = step["task"]
            agent_type = step["agent_type"]
            
            print(f"\n[Step {step_id}] Sub-task: {sub_task}")
            
            # 3. Assistant manages the delegation
            self.assistant.act(sub_task)
            
            # 4. Delegate to specialized agent if available
            if agent_type in self.specialized_agents:
                specialized_agent = self.specialized_agents[agent_type]
                print(f"Assistant delegating to: {specialized_agent.name} ({agent_type})")
                result = specialized_agent.act(sub_task)
                print(f"Specialized Agent Result: {result}")
                
                # 5. Conditional Verification
                # Verification is triggered if explicitly required or if the sub-task involves high-risk info gathering
                if require_verification or "information" in sub_task.lower():
                    if "VerificationAgent" in self.specialized_agents:
                        verifier = self.specialized_agents["VerificationAgent"]
                        print(f"--- Conditional Activation: {verifier.name} (VerificationAgent) ---")
                        verification_report = verifier.act(result)
                        print(f"Verification Result: {verification_report}")
                        result = f"{result}\n\n[Verification Report]\n{verification_report}"
                
                # 6. Assistant updates state
                self.assistant.update_state(f"step_{step_id}_result", result)
                
                # 7. Knowledge Management (Obsidian)
                if "ObsidianAgent" in self.specialized_agents:
                    obsidian_agent = self.specialized_agents["ObsidianAgent"]
                    print(f"Assistant delegating to: {obsidian_agent.name} (ObsidianAgent)")
                    obsidian_agent.act({"title": f"Step_{step_id}_Result", "content": result})
            else:
                print(f"Warning: No specialized agent registered for type: {agent_type}")
        
        print("\n--- Multi-Agent Orchestration Completed ---")
