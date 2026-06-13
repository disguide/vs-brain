from src.agents.info_gathering_agent import InfoGatheringAgent
from src.harness.harness import AgentHarness
from src.tools.web_search import web_search
from src.tools.specialized_search import news_search, extract_webpage_content

def main():
    # 1. Initialize the specialized agent
    agent = InfoGatheringAgent(name="InfoSeeker", model_name="gpt-4-turbo")

    # 2. Initialize the harness and register tools
    harness = AgentHarness(agent)
    harness.register_tool("web_search", web_search, required_permissions=["read_only"])
    harness.register_tool("news_search", news_search, required_permissions=["read_only"])
    harness.register_tool("extract_webpage", extract_webpage_content, required_permissions=["read_only"])

    # 3. Define the information gathering task
    task = "Latest developments in autonomous AI agent frameworks June 2026"

    # 4. Run the agentic loop via the harness
    print("--- Demonstrating Information Gathering Agent ---")
    result = harness.run_loop(task)
    
    print(f"\nFinal Agent Result:\n{result}")
    print("-------------------------------------------------")

if __name__ == "__main__":
    main()
