# vs-brain Architecture

The `vs-brain` framework is designed around the principle that an AI agent is composed of two distinct parts: the **Model** (the intelligence) and the **Harness** (the runtime environment) [1]. This separation of concerns is crucial for building reliable, secure, and observable autonomous systems.

## Core Components

### 1. The Model
The Model represents the Large Language Model (LLM) that provides the reasoning and generative capabilities. `vs-brain` is designed to be provider-neutral, allowing integration with various models (e.g., OpenAI, Anthropic, open-source models). The model's primary role is to propose actions and tool calls based on its context.

### 2. The Harness
The Harness is the deterministic runtime layer that wraps the LLM. It is responsible for validating, authorizing, executing, and logging every action the model proposes [2]. Key responsibilities include:
*   **Execution Engine**: Manages the agentic loop, handling the flow of information between the model and the environment.
*   **Tool Registry**: Maintains a list of available tools and their schemas.
*   **Permission Resolver**: Enforces security policies, ensuring the model only executes authorized actions.
*   **Context Builder**: Manages the context window, handling memory retrieval and compaction to prevent context rot [1].

## The Agentic Loop

The core of the `vs-brain` architecture is the agentic loop, which follows a strict sequence:
1.  **Context Assembly**: The harness gathers relevant information (system policies, memory, task details) and presents it to the model.
2.  **Model Proposal**: The model analyzes the context and proposes an action, typically in the form of a structured tool call.
3.  **Validation & Authorization**: The harness validates the tool call against its schema and checks if the agent has the necessary permissions [2].
4.  **Execution**: If authorized, the harness executes the tool.
5.  **Observation**: The harness captures the result of the tool execution (success, failure, or timeout) and feeds it back into the context for the next iteration.

## Security and Permissions

Security is a foundational element of `vs-brain`. The framework implements a risk-based permission model:
*   **Read-only**: Actions that only retrieve data can often be executed autonomously.
*   **Draft**: Actions that prepare changes but do not apply them (e.g., drafting an email).
*   **External Write**: Actions that modify external systems or communicate externally require explicit human approval [2].

This "draft-commit" pattern ensures that dangerous actions are always reviewed before execution.

## References
[1] [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
[2] [AI Agent Best Practices: Production-Ready Harness Engineering (2026 Guide)](https://medium.com/@tort_mario/ai-agent-best-practices-production-ready-harness-engineering-2026-guide-c1236d713fac)
