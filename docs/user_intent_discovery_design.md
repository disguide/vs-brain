# User Intent Discovery Agent Design

The **User Intent Discovery Agent** is the primary entry point for the `vs-brain` framework. Its critical role is to bridge the gap between vague or high-level user requests and the structured, actionable goals required for multi-agent orchestration.

## Objectives

*   **Clarification**: Engaging in a dialogue with the user to resolve ambiguities in their request.
*   **Goal Extraction**: Identifying the core objective the user wants to achieve.
*   **Success Condition Definition**: Defining clear, measurable criteria for what constitutes a successful outcome.
*   **Context Gathering**: Collecting necessary background information or constraints from the user.
*   **Adaptability**: Handling vague, informal, or incomplete language effectively.

## Interaction Strategy

The agent employs a "Question and Refine" strategy:
1.  **Initial Analysis**: Analyzes the user's first input to identify missing or ambiguous elements.
2.  **Proactive Questioning**: Asks targeted questions to fill information gaps (e.g., "What specific domain are you interested in?", "What would a successful report look like for you?").
3.  **Refinement Loop**: Continues the dialogue until a clear goal and success conditions are established.
4.  **Confirmation**: Presents the refined goal and success conditions back to the user for final approval.

## Workflow Integration

This agent operates **before** any other specialized agents. Only after the User Intent Discovery Agent has confirmed the goal does the Orchestrator begin task decomposition and delegation.

## Permission and Risk

As a purely conversational agent, its actions are "Read-only" and "Draft". It is considered low-risk.
