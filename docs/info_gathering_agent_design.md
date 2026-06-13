# Information Gathering Agent Design

The Information Gathering Agent is a specialized component within the `vs-brain` framework designed to efficiently and reliably retrieve up-to-date information from various external sources. It serves as a foundational step in many complex workflows, providing the raw data necessary for analysis, reasoning, and decision-making.

## Objectives

*   **Efficiency**: Rapidly identify and retrieve relevant information.
*   **Reliability**: Ensure the information gathered is accurate and from credible sources.
*   **Comprehensiveness**: Cover a wide range of sources, including web search, news, and specialized APIs.
*   **Up-to-date**: Prioritize recent information to overcome LLM knowledge cutoffs.

## Agent Architecture

The Information Gathering Agent will extend the `BaseAgent` class and implement the following specialized logic:

*   **Query Expansion**: Automatically generate multiple search query variants to broaden the search scope and improve coverage.
*   **Source Prioritization**: Evaluate and prioritize search results based on credibility and relevance.
*   **Information Extraction**: Extract key information from search results, handling various formats (e.g., HTML, PDF, text).
*   **Summarization and Synthesis**: Summarize the gathered information to provide a concise and relevant output for subsequent steps in a workflow.

## Specialized Tools

The agent will utilize a set of specialized tools integrated into the `vs-brain` harness:

1.  **Web Search Tool**: Provides access to general web search results.
2.  **News Search Tool**: Specifically targets news articles and recent updates.
3.  **Webpage Extraction Tool**: Efficiently extracts markdown content from specified URLs.
4.  **Source Credibility Checker**: Evaluates the reliability of information sources.

## Workflow Integration

The Information Gathering Agent is typically the first step in a multi-agent orchestration. Its output—a structured summary of gathered information—serves as the input for subsequent agents (e.g., Data Analysis Agent, Drafting Agent).

## Permission and Risk

As an information gathering tool, the agent primarily performs "Read-only" actions. These actions are generally considered low-risk and can be executed autonomously by the harness after validation. However, the harness will still monitor for excessive tool usage or attempts to access unauthorized domains.
