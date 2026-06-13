# Tools and Permissions in vs-brain

Tools are essential components that extend the capabilities of AI agents beyond the inherent knowledge of the Large Language Model (LLM). In the `vs-brain` framework, tools enable agents to interact with the external environment, perform specific actions, and access real-time information. However, the integration and execution of these tools must be governed by a robust permission system to ensure security, reliability, and controlled autonomy [1].

## What are Tools?

Tools are functions or services that an agent can invoke to perform specific tasks. These can range from simple utilities like web search or file operations to complex integrations with external APIs (e.g., CRM systems, databases, communication platforms). The `vs-brain` framework emphasizes the use of **narrow, typed tools** with structured schemas, rather than broad, generic tools [2]. This approach enhances predictability, allows for rigorous validation, and minimizes the risk of unintended actions.

## Tool Integration

Integrating a tool into the `vs-brain` harness involves:
1.  **Defining a Clear Schema**: Each tool must have a well-defined input and output schema, allowing the harness to validate the agent's proposed tool calls and parse the results effectively.
2.  **Registering with the Harness**: Tools are registered with the `AgentHarness`, making them available for discovery and use by agents. This registration includes associating the tool with specific permissions.
3.  **Encapsulating Logic**: The internal logic of a tool should be self-contained and focused on a single responsibility.

## Permission Management and Risk Assessment

The `vs-brain` framework implements a multi-level permission system to manage the risks associated with tool execution. This system is based on the principle that **the model proposes, but the harness executes**, with explicit checks at each step [2].

### Risk Levels
Tools and actions are categorized into different risk levels, which dictate the necessary authorization process:

*   **Read-only (Autonomous)**: Actions that only retrieve information and have no side effects on external systems. These can often be executed autonomously by the agent after validation.
*   **Draft (Internal Simulation)**: Actions that prepare changes or generate content but do not apply them externally. These might involve internal simulations or generating proposals that require human review before externalization.
*   **External Write (Requires Approval)**: Actions that modify external systems, send communications, or perform financial transactions. These are considered high-risk and **always require explicit human approval** before execution. This implements a 
"draft-commit" pattern, where dangerous actions are first drafted and then explicitly committed [2].

### Permission Matrix

The harness maintains a permission matrix that maps tools to required risk levels and approval workflows. This matrix is configurable and allows for fine-grained control over agent capabilities.

| Action Type       | Risk Level         | Approval Required | Description                                                                 |
| :---------------- | :----------------- | :---------------- | :-------------------------------------------------------------------------- |
| `read_data`       | Read-only          | No                | Accessing internal or external data without modification.                   |
| `generate_report` | Draft              | No                | Creating internal documents or reports.                                     |
| `send_email`      | External Write     | Yes               | Sending emails to external recipients.                                      |
| `update_database` | External Write     | Yes               | Modifying records in a database.                                            |
| `deploy_code`     | External Write     | Yes               | Deploying code to production environments.                                  |

## References
[1] [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
[2] [AI Agent Best Practices: Production-Ready Harness Engineering (2026 Guide)](https://medium.com/@tort_mario/ai-agent-best-practices-production-ready-harness-engineering-2026-guide-c1236d713fac)
