# Context and Memory Management in vs-brain

Effective context and memory management are critical for the performance, coherence, and long-term learning capabilities of AI agents within the `vs-brain` framework. Large Language Models (LLMs) have finite context windows, and efficiently managing the information presented to them is essential to prevent "context rot" and ensure agents can maintain state and learn across interactions [1].

## The Importance of Context

Context refers to all the information available to the LLM at any given moment to inform its reasoning and actions. This includes system prompts, tool descriptions, conversation history, retrieved knowledge, and current task details. A well-managed context ensures the agent has access to relevant information without being overwhelmed by noise or exceeding its token limits.

## Memory Mechanisms

`vs-brain` employs several mechanisms to manage agent memory:

1.  **Short-Term Memory (Context Window)**: This is the immediate working memory of the agent, directly fed into the LLM. It contains the most recent and relevant information for the current step of the agentic loop.
2.  **Long-Term Memory (Filesystem & Databases)**: For durable storage and context management, `vs-brain` leverages filesystems and potentially databases. This allows agents to:
    *   **Persist Work**: Store intermediate outputs, plans, and observations across sessions.
    *   **Offload Information**: Move less critical or large pieces of information out of the immediate context window, retrieving them only when needed.
    *   **Collaborate**: Use shared filesystems as a common ground for multiple agents or human-agent collaboration [1].
3.  **Retrieval Augmented Generation (RAG)**: Agents can access external knowledge bases or perform web searches to retrieve up-to-date information that was not present in their training data or current context. This is crucial for overcoming knowledge cutoffs and accessing real-time data [1].

## Context Compaction Strategies

To combat context rot and ensure efficient use of the LLM's context window, `vs-brain` implements intelligent compaction strategies:

*   **Summarization**: Long conversation histories or detailed observations can be summarized to retain key information while reducing token count.
*   **Offloading**: Large tool outputs or less frequently accessed data can be stored in long-term memory (e.g., filesystem) and only referenced or retrieved when explicitly required by the agent.
*   **Layered Context**: Context is assembled in layers, from most stable (system policies) to least stable (JIT-retrieved tool outputs). This allows for efficient prompt caching and ensures that critical, unchanging information is always available [2].
*   **Preserving Active State**: During compaction, the harness prioritizes preserving active state elements such as plans, approvals, and to-do lists, rather than simply truncating chat history. This ensures the agent maintains its operational coherence [2].

## References
[1] [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
[2] [AI Agent Best Practices: Production-Ready Harness Engineering (2026 Guide)](https://medium.com/@tort_mario/ai-agent-best-practices-production-ready-harness-engineering-2026-guide-c1236d713fac)
