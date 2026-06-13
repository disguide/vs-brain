# The Agentic Loop in vs-brain

The agentic loop is the fundamental operational cycle that enables AI agents within the `vs-brain` framework to perceive, reason, act, and learn continuously. It is a structured process designed to ensure reliable and controlled execution of tasks by separating the model's generative capabilities from the harness's deterministic runtime responsibilities [1].

## Core Principles of the Agentic Loop

1.  **Model Proposes, Harness Executes**: The Large Language Model (LLM) proposes actions or tool calls, but the `vs-brain` harness is solely responsible for validating, authorizing, and executing these proposals. This prevents the LLM from directly interacting with the environment in an uncontrolled manner [2].
2.  **Structured Observations**: Every action taken by the harness, whether successful or a failure (e.g., permission denied, timeout), returns a structured observation to the agent. This ensures the agent always receives clear feedback to inform its next steps [2].
3.  **Budgeting and Termination**: To prevent uncontrolled execution and manage costs, the agentic loop incorporates various budgets, including step limits, time limits, token limits, and cost limits. When any budget is exhausted, the harness gracefully terminates the loop and returns a structured failure [2].

## Phases of the Agentic Loop

The `vs-brain` agentic loop can be broken down into the following sequential phases:

### 1. Context Assembly
Before each iteration, the harness constructs a comprehensive context for the LLM. This involves:
*   **System Policies**: Injecting stable, system-level instructions and constraints.
*   **Agent Skill Definitions**: Providing relevant skill descriptions and tool schemas.
*   **User Session Instructions**: Incorporating task-specific or conversation-specific guidance.
*   **JIT-Retrieved Information**: Fetching up-to-date data from memory or external tools as needed [2].

### 2. Model Proposal
The LLM, based on the assembled context, generates a proposal for its next action. This proposal is typically a structured tool call, specifying the tool to be used and its arguments.

### 3. Validation and Authorization
Upon receiving a proposal, the harness performs critical checks:
*   **Schema Validation**: Verifies that the proposed tool call adheres to the defined schema of the tool.
*   **Permission Check**: Consults the permission matrix to determine if the agent is authorized to execute the proposed tool with its given parameters, considering the associated risk level [2].

### 4. Execution
If the proposal passes validation and authorization, the harness executes the specified tool. This execution occurs within a safe, isolated environment (e.g., a sandbox) to prevent unintended side effects [1].

### 5. Observation and Feedback
After execution, the harness captures the outcome and transforms it into a structured observation. This observation is then appended to the agent's memory and included in the context for the subsequent iteration of the loop. This feedback mechanism allows the agent to self-correct and adapt its behavior [1].

### 6. Context Compaction (Optional)
If the context window approaches its limit, the harness employs compaction strategies to summarize or offload less critical information while preserving essential state (e.g., active approvals, plans). This prevents 
context rot and ensures efficient use of the LLM's context window [1].

## References
[1] [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
[2] [AI Agent Best Practices: Production-Ready Harness Engineering (2026 Guide)](https://medium.com/@tort_mario/ai-agent-best-practices-production-ready-harness-engineering-2026-guide-c1236d713fac)
