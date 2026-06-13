# LLM Wiki Architecture: The AI Second Brain

This document defines the integrated architecture of the `vs-brain` framework, incorporating the "AI Second Brain" stack and industry-leading multi-agent patterns.

## 1. Core Philosophy: The LLM Wiki
The central idea is to transform messy, unstructured source material into **structured, compounding knowledge**. This is achieved through a multi-layered approach to information capture, organization, and retrieval.

## 2. The 4 Supporting Layers

### Layer 1: Setup & Implementation (Obsidian Skills)
*   **Source**: [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
*   **Role**: Provides the "muscles" for the agent to interact with Obsidian.
*   **Integration**: Standardized agent skills for managing frontmatter, JSON Canvas, and Obsidian CLI operations.

### Layer 2: Folder Structure (PARA)
*   **Source**: [Tiago Forte's PARA Method](https://fortelabs.com/blog/para/)
*   **Role**: Provides the organizational "skeleton".
*   **Structure**:
    *   **Projects**: Active tasks with a deadline.
    *   **Areas**: Ongoing responsibilities (e.g., "Health", "Finances").
    *   **Resources**: Topics of interest for the future.
    *   **Archive**: Completed or inactive items.

### Layer 3: Structure & Refinement (Graphify)
*   **Source**: [safishamsi/graphify](https://github.com/safishamsi/graphify)
*   **Role**: Maps the knowledge graph and identifies relationships.
*   **Integration**: Visualizes clusters, important nodes, and weak links. Helps the agent understand the "weight" and connections within the vault.

### Layer 4: Retrieval for Agents (QMD)
*   **Source**: [tobi/qmd](https://github.com/tobi/qmd)
*   **Role**: High-performance retrieval engine.
*   **Integration**: On-device hybrid search (BM25 + Vector) specifically optimized for Markdown. Allows agents to query the vault with high precision and low token usage.

## 3. Multi-Agent Orchestration Integration

### Agent-MCP Integration
*   **Role**: Shared persistent memory bank.
*   **Mechanism**: Uses the Model Context Protocol to synchronize the "brain" state across multiple agents.

### CrewAI & 500+ Agents Integration
*   **Role**: Specialized Personas.
*   **Mechanism**: Adopts role-based patterns for agents (e.g., Researcher, Verifier, Librarian) and draws from a library of 500+ proven agent use cases for specific tasks.

## 4. The Integrated Workflow

1.  **Discovery**: `UserIntentDiscoveryAgent` clarifies the goal.
2.  **Planning**: `OrchestratorAgent` (using CrewAI patterns) decomposes the task.
3.  **Execution**:
    *   `InfoGatheringAgent` retrieves up-to-date data.
    *   `VerificationAgent` ensures robustness.
    *   `ObsidianAgent` (using PARA & Obsidian Skills) captures and organizes the knowledge.
4.  **Refinement**: `Graphify` logic identifies links, and `QMD` enables efficient retrieval for subsequent steps.
5.  **Compounding**: Each task result is linked and stored in the **LLM Wiki**, making the "brain" smarter over time.
